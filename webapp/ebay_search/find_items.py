import isodate
from flask_login import current_user

from webapp.utils import (
    get_finding_headers, get_shopping_headers, post_ebay_finding_request, post_ebay_request,
)
from webapp.ebay_search.models import db, Ebay_Categories


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
    elif parsed_item:
        field_value = parsed_item.text
    else:
        field_value = ''
    return field_value


def find_items_advanced(query, categiryid, page_number=1, user_filters_list=[]):
    """
    Функция поиска товаров на Ebay по поисковому запросу и выбранной категории товаров
    """
    headers = get_finding_headers("findItemsAdvanced")
    if user_filters_list:
        filters = make_filter_string_for_finding_request(user_filters_list)
    else:
        filters = None
    data = f"""
    <findItemsAdvancedRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
        <categoryId>{categiryid}</categoryId>
        <outputSelector>AspectHistogram</outputSelector>
        <descriptionSearch>true</descriptionSearch>
        <keywords>{query}</keywords>
        <itemFilter>
            <name>ListingType</name>
            <value>Auction</value>
            <value>AuctionWithBIN</value>
        </itemFilter>
        <aspectFilter>
            {filters}
        </aspectFilter>
        <paginationInput>
            <entriesPerPage>50</entriesPerPage>
            <pageNumber>{page_number}</pageNumber>
        </paginationInput>
        <sortOrder>EndTimeSoonest</sortOrder>
    </findItemsAdvancedRequest>"""
    print(data)
    response_soup = post_ebay_finding_request(headers, data)
    print(response_soup)
    # Получаем количество страниц из ответа на запрос
    total_pages = int(response_soup.find('totalpages').text)
    # Обрабатываем результаты поискового запроса
    all_items = response_soup.find_all('item')
    search_result = []
    for item in all_items:
        pars_item = {}
        for key, value in soup_keys.items():
            pars_item[key] = parsfield(item, value)
        search_result.append(pars_item)

    # Обрабатываем фильтры для уточнения поискового запроса
    histogram_container = response_soup.find('aspecthistogramcontainer')
    subcategory = histogram_container.find('domaindisplayname').text
    # получаем id подкатегории из базы данных
    # for categoryid in db.session.query(Ebay_Categories.categoryid).filter_by(categoryname=subcategory).first():
    subcategory_id = db.session.query(Ebay_Categories.categoryid).filter_by(categoryname=subcategory).first().categoryid

    all_aspects = histogram_container.find_all('aspect')
    histogram_container_data = []
    for aspect in all_aspects:
        aspect_data = {}
        aspect_data['aspect_name'] = aspect['name']
        histogram_values = aspect.find_all('valuehistogram')
        histogram_values_data = []
        for value in histogram_values:
            value_data = {}
            value_data['value_name'] = value['valuename']
            value_data['count'] = value.find('count').text
            histogram_values_data.append(value_data)
        aspect_data['aspect_data'] = histogram_values_data
        histogram_container_data.append(aspect_data)
    return search_result, total_pages, subcategory, subcategory_id, histogram_container_data


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


def get_user_filters_request(filters_request):
    """
    Функция преобразует фильтры из поискового запроса в список
    """
    filters_data = filters_request.split(';')
    filters_data.remove(filters_data[-1])
    user_filters_request = []
    for filters in filters_data:
        filters = filters.replace('&', '&amp;')
        category_filters = {}
        one_category_filters = filters.split(':')
        category_filters['filter_name'] = one_category_filters[0]
        category_filters['filter_values'] = one_category_filters[1].split(',')
        user_filters_request.append(category_filters)
    return user_filters_request

def make_filter_string_for_finding_request(user_filters_request):
    """
    Функция приобразует список фильтров поискового запроса в строку формата
    data для направление запроса на API EBay
    """
    test_string = ''
    for filters in user_filters_request:
        if not len(test_string):
            test_string += f"<aspectName>{filters['filter_name']}</aspectName>"
        else:
            test_string += '\n' + f"            <aspectName>{filters['filter_name']}</aspectName>"
        for value in filters['filter_values']:
            test_string += '\n' + f"            <aspectValueName>{value}</aspectValueName>"
    return test_string


def delete_filter_from_request(filters_request, value):
    """
    Функция удаляет фильтр из списка избранных фильтров пользователя по запросу с html
    """
    user_filters_request = get_user_filters_request(filters_request)
    for filters in user_filters_request:
        if len(filters['filter_values']) == 1 and value in filters['filter_values']:
            user_filters_request.remove(filters)
            del filters
        elif value in filters['filter_values']:
            filters['filter_values'].remove(value)
    return user_filters_request
