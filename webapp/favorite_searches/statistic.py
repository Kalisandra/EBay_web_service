from datetime import datetime, timedelta

import isodate

from webapp import db
from webapp.ebay_search.find_items import (
    find_items_advanced,
    get_user_filters_request,
    get_item)
from webapp.favorite_searches.models import FavoriteSearches, StatisticItems
from webapp.utils import get_shopping_headers, post_ebay_request


def get_ebay_time(token):
    """
    Функция запрашивает текущее официальное время Ebay
    """
    headers = get_shopping_headers("GeteBayOfficialTime")
    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GeteBayOfficialTimeRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{token}</eBayAuthToken>
    </RequesterCredentials>
    </GeteBayOfficialTimeRequest>"""
    response_soup = post_ebay_request(headers, data)
    current_time = response_soup.find('timestamp').text
    current_time = isodate.parse_datetime(
        current_time).strftime('%Y-%m-%d %H:%M:%S')
    current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    return current_time


def get_item_to_statistic():
    """
    Функция запрашивает в базе 'Избранные поиски' статус ведения статистики, и если он активный
    делает соответствующий поисковый запрос на Ebay и записывает в отдельную таблицу уникальные
    (не встречающиеся в базе) лоты
    """
    # запрос к базе FavoriteSearches для выборки избранных поисков
    # с подключенным ведением статистики
    favorite_search_with_statistic = FavoriteSearches.query.filter(
        FavoriteSearches.statistic_status == True).all()
    for search in favorite_search_with_statistic:
        # проверяем дату активации начала статистики
        if search.statistic_start_date + timedelta(days=7) > datetime.now():
            # направляем поисковый запрос на Ebay
            query_id = search.id
            query = search.user_query
            categoryid = search.chosen_categoryid
            user_filters_list = get_user_filters_request(search.filter_request)
            search_result = find_items_advanced(
                query, categoryid, user_filters_list=user_filters_list)[0]
        # Записываем уникальные лоты в отдельную таблицу в базе
            for item in search_result:
                item_exists = StatisticItems.query.filter(
                    StatisticItems.item_id == item['item_id']).count()
                if not item_exists:
                    new_statistic_item = StatisticItems(
                        query_id=query_id,
                        item_id=item['item_id'],
                        item_name=item['title'],
                        item_current_price=item['item_current_price_converted'],
                        end_time=datetime.strptime(
                            item['end_time'], '%Y-%m-%d %H:%M:%S'),
                        item_url=item['view_item_url'])
                    db.session.add(new_statistic_item)
                    db.session.commit()


def get_final_price():
    """
    Функция делает выборку лотов по таблице базы данных "statistic_items" не имеющих записи в
    поле "final_price".
    Далее делает запрос времени Ebay (для каждого пользователя только один раз в рамках одного
    запроса, чтобы уменьшить время работы функции) и если время Ebay больше времени завершения
    аукциона делат запрос на Ebay об информации о лоте из которого получает итоговую цену и
    количество ставок
    """
    items_without_final_price = StatisticItems.query.filter(StatisticItems.final_price.is_(None))
    current_user_token = ""
    time = ""
    for item in items_without_final_price:
        user_token = item.favorite_searches.user.token
        if current_user_token != user_token:
            current_user_token = user_token
            time = get_ebay_time(user_token)
            if item.end_time < time:
                pars_item = get_item(item.item_id, user_token)
                item.final_price = pars_item['item_current_price_converted']
                item.bids = pars_item['bid_count']
                db.session.commit()
        elif current_user_token == user_token and item.end_time < time:
            pars_item = get_item(item.item_id, user_token)
            item.final_price = pars_item['item_current_price_converted']
            item.bids = pars_item['bid_count']
            db.session.commit()
