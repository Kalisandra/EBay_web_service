from flask import Blueprint, flash, render_template, request

from webapp.ebay_search.find_items import (
    find_items_advanced, add_to_watch_list, get_user_watch_list,
    remove_from_user_watch_list, get_user_filters_request,
)
from webapp.ebay_search.models import EbayCategories
from webapp.user.decorators import user_required


blueprint = Blueprint('search', __name__, url_prefix='/search')


@blueprint.route('/')
@user_required
def search():
    # получаем категории товаров Ebay из базы данных для отображения на поисковой странице
    categories = EbayCategories.query.filter_by(
        category_level=1)
    # получаем результаты запроса от пользователя из поисковой строки
    q = request.args.get('q')
    # получаем выбранную категорию со страницы поиска
    chosen_categoryid = request.args.get('categoryid')
    # получаем номер выбранной страницы, по умолчанию номер страницы = 1
    page_number = request.args.get('pagenumber')
    if not page_number:
        page_number = 1
    # получаем значения выбранных фильтров расширенного поиска
    filters_request = request.args.get('filters')
    # получаем значение фильтра, удаляемое из поискового запроса
    if filters_request:
        user_filters_list = get_user_filters_request(filters_request)
    else:
        user_filters_list = None
    # При направлении любого поискового запроса получаем с Ebay список 
    # избранных лотов пользователя
    if q:
        watch_items = get_user_watch_list()


    # обрабатываем поисковый запрос пользователя, номер выбранной страницы,
    # фильтры и передаем его в html
    if q:
        (results, total_pages, subcategory, subcategory_id, histogram_container_data
            ) = find_items_advanced(
            q,
            chosen_categoryid,
            page_number=page_number,
            user_filters_list=user_filters_list)

    search_request = {
        'title': 'Результаты поиска' if q else None,
        'categories': categories,
        'pagenumber': page_number,
        'userfilterslist': user_filters_list,
        'watch_list': watch_items if q else None,
        'results': results if q else None,
        'totalpages': total_pages if q else None,
        'subcategory': subcategory if q else None,
        'subcategoryid': subcategory_id if q else None,
        'histogram_container_data': histogram_container_data if q else None,
    }

    return render_template(
        'ebay_search/search.html',
        **search_request)


@blueprint.route('/add_to_watch_list')
def add_to():
    item_id = request.args.get('itemid')
    if item_id:
        add_to_watch_list(item_id)

        return render_template('ebay_search/add_to_watch_list.html')


@blueprint.route('/watch_list')
@user_required
def open_watch_list():
    watch_items = get_user_watch_list()
    return render_template(
        'ebay_search/watch_list.html', watch_list=watch_items)


@blueprint.route('/remove_item')
def remove_from():
    item_id = request.args.get('itemid')
    if item_id:
        remove_from_user_watch_list(item_id)
        return render_template('ebay_search/remove_from_watch_list.html')


@blueprint.context_processor
def filter_processor():
    def delete_filter_from_request(filters_request, value):
        """
        Функция удаляет фильтр из списка избранных фильтров
        пользователя по запросу с html
        """
        user_filters_request = get_user_filters_request(filters_request)
        for filters in user_filters_request:
            if (len(filters['filter_values']) == 1 and
                    value in filters['filter_values']):
                user_filters_request.remove(filters)
            elif value in filters['filter_values']:
                filters['filter_values'].remove(value)
        new_filters_request = ''
        for filters in user_filters_request:
            new_filters_request += f"{filters['filter_name']}:"
            for value in filters['filter_values']:
                new_filters_request += f"{value};"
        return new_filters_request
    return dict(new_filters_request=delete_filter_from_request)
