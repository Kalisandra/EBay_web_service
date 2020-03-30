from datetime import datetime

from flask import flash
from flask_login import current_user

from webapp.utils import get_finding_headers, get_shopping_headers, \
    post_ebay_finding_request, post_ebay_request



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
    </findItemsAdvancedRequest>"""

    response_soup = post_ebay_finding_request(headers, data)
    all_items = response_soup.find_all('item')
    search_result = []
    for item in all_items:
        item_id = item.find('itemid').text
        title = item.find('title').text
        category_id = item.find('categoryid').text
        gallery_url = item.find('galleryurl').text
        view_item_url = item.find('viewitemurl').text
        item_country = item.find('country').text
        shipping_type = item.find('shippingtype').text
        item_current_price = item.find('currentprice').text
        item_currency = item.find('currentprice')['currencyid']
        bid_count = item.find('bidcount').text
        selling_state = item.find('sellingstate').text
        time_left = item.find('timeleft').text
        end_time = item.find('endtime').text
        listing_type =item.find('listingtype').text 
        condition_id = item.find('conditionid').text
        condition_display_name = item.find('conditiondisplayname').text
        # конвертируем время из стандарта ISO 8601 в datetime


    # записываем результаты поиска в список
        search_result.append({
            'item_id': item_id,
            'title': title,
            'category_id': category_id,
            'gallery_url': gallery_url,
            'view_item_url': view_item_url,
            'item_country': item_country,
            'shipping_type': shipping_type,
            'item_current_price': item_current_price,
            'item_currency': item_currency,
            'bid_count': bid_count,
            'selling_state': selling_state,
            'time_left': time_left,
            'end_time': end_time,
            'listing_type': listing_type,
            'condition_id': condition_id,
            'condition_display_name': condition_display_name,
        })

    return search_result


def add_to_watch_list(itemid):
    headers = get_shopping_headers('AddToWatchList')
    token = current_user.token
    data = f"""
    <AddToWatchListRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{token}</eBayAuthToken>
    </RequesterCredentials>
    <ItemID>{itemid}</ItemID>
    </AddToWatchListRequest>
    """

    response_soup = post_ebay_request(headers, data)
    if response_soup.find('ack').text == 'Success':
        return flash('Лот успешно добавлен в "Избранное"')
    else:
        return flash('Лот не добавлен в "Избранное". Результаты поиска устарели')