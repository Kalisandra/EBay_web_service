

def search():
    # получаем категории товаров Ebay из базы данных для отображения на поисковой странице
    categories = EbayCategories.query.filter(
        EbayCategories.category_level == 1)
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
        (results,
        total_pages,
        subcategory,
        subcategory_id,
        histogram_container_data) = find_items_advanced(
            q,
            chosen_categoryid,
            page_number=page_number,
            user_filters_list=user_filters_list,
            )

search_request = {
    'title': 'Результаты поиска' if q else None
    'categories': categories,
    'watch_list': watch_item if q else None
    'results': results if q else None
    
    'total_pages': total_pages if q else None
    'userfilterslist': user_filters_list
}





        page_number = ''
        subcategory = ''
        subcategory_id = ''
        histogram_container_data = ''

    return render_template(
        'ebay_search/search.html',
        **search_request)


        title=title, +
        results=results, +
        categories=categories, +
        totalpages=total_pages,
        watch_list=watch_items, +
        pagenumber=page_number,
        subcategory=subcategory,
        subcategoryid=subcategory_id,
        histogram_container_data=histogram_container_data,
        userfilterslist=user_filters_list, +
    