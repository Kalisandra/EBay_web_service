from datetime import datetime

import isodate
from flask_login import current_user

from webapp.utils import get_finding_headers, get_shopping_headers, \
    post_ebay_finding_request, post_ebay_request


soup_keys = {
    'item_id': 'itemid',
    'title': 'title',
    'category_id': 'categoryid',
    'gallery_url': 'galleryurl',
    'view_item_url': 'viewitemurl',
    'item_country': 'itemcountry',
    'shipping_type': 'shippingtype',
    'item_current_price_converted': 'convertedcurrentprice',
    'item_current_price': 'currentprice',
    'bid_count': 'bidcount',
    'selling_state': 'sellingstate',
    'time_left': 'timeleft',
    'end_time': 'endtime',
    'listing_type': 'listingtype',
    'condition_id': 'conditionid',
    'condition_display_name': 'conditiondisplayname',
}

def parsfield(item, value):
    parsed_item = item.find(value)
    if parsed_item and value == 'endtime':
        field_value = parsed_item.text
        field_value = isodate.parse_datetime(field_value).strftime('%Y-%m-%d %H:%M:%S')
    elif parsed_item and value == 'timeleft':
        field_value = parsed_item.text
        field_value = str(isodate.parse_duration(field_value))
<<<<<<< HEAD
        return field_value
=======
>>>>>>> 6191ff9745afeea0dfbd23bc88381563d568ec91
    elif parsed_item:
        field_value = parsed_item.text
    else:
        field_value = ''
    return field_value


def find_items_advanced(query, categiryid):
    headers = get_finding_headers("findItemsAdvanced")
    data = f"""
    <findItemsAdvancedRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
        <categoryId>{categiryid}</categoryId>
        <descriptionSearch>true</descriptionSearch>
        <keywords>{query}</keywords>
        <itemFilter>
            <name>ListingType</name>
            <value>Auction</value>
            <value>AuctionWithBIN</value>
        </itemFilter>
        <sortOrder>EndTimeSoonest</sortOrder>
    </findItemsAdvancedRequest>"""

    response_soup = post_ebay_finding_request(headers, data)
    all_items = response_soup.find_all('item')
    search_result = []
    for item in all_items:
        pars_item = {}
        for key, value in soup_keys.items():
            pars_item[key] = parsfield(item, value)
        search_result.append(pars_item)
    return search_result


def add_to_watch_list(itemid):
    headers = get_shopping_headers('AddToWatchList')
    token = current_user.token
    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <AddToWatchListRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{token}</eBayAuthToken>
    </RequesterCredentials>
    <ItemID>{itemid}</ItemID>
    </AddToWatchListRequest>
    """

    response_soup = post_ebay_request(headers, data)
    if response_soup.find('ack').text == 'Success':
        return print('Лот успешно добавлен в "Избранное"')
    else:
        return print('Лот не добавлен в "Избранное". Результаты поиска устарели')

def get_user_watch_list():
    """
    Функция через запрос к API Ebay получает список избранных лотов
    """
    headers = get_shopping_headers('GetMyeBayBuying')
    token = current_user.token
    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GetMyeBayBuyingRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{token}</eBayAuthToken>
    </RequesterCredentials>
    <WatchList>
        <Include>true</Include>
    </WatchList>
    </GetMyeBayBuyingRequest>
    """
    response_soup = post_ebay_request(headers, data)
    if response_soup.find('ack').text == 'Success':
        user_watch_list = []
        all_items = response_soup.find_all('item')
        for item in all_items:
            pars_watch_item = {}
            for key, value in soup_keys.items():
                pars_watch_item[key] = parsfield(item, value)
            user_watch_list.append(pars_watch_item)
        return user_watch_list


def remove_from_user_watch_list(itemid):
    """
    Фунция для удаления товара из списка "Избранное" пользователя.
    В качестве аргумента передается id товара
    """
    headers = get_shopping_headers('RemoveFromWatchList')
    token = current_user.token
    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <RemoveFromWatchListRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{token}</eBayAuthToken>
    </RequesterCredentials>
    <ItemID>{itemid}</ItemID>
    </RemoveFromWatchListRequest>
    """

    response_soup = post_ebay_request(headers, data)
    if response_soup.find('ack').text == 'Success':
        return print('Лот успешно удален из списка избранных товаров')
    else:
        return print('Не получилось удалить лот из списка избоанных товаров.\
            Обновите страниуц и повторите заново')