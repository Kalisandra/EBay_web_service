def search():
    # получаем категории товаров Ebay из базы данных
    # categories = EbayCategories.query.filter(
    #     EbayCategories.category_level == 1)
    categories = EbayCategories.query.filter_by(
        category_level=1)
    # получаем результаты запроса от пользователя из поисковой строки
    q = request.args.get('q')
    # получаем выбранную категорию со страницы поиска
    chosen_categoryid = request.args.get('categoryid')
    # получаем номер выбранной страницы, по умолчанию номер страницы = 1
    page_number = request.args.get('pagenumber')
    # получаем значения выбранных фильтров расширенного поиска
    filters_request = request.args.get('filters')
    print(filters_request)
    # получаем значение фильтра, удаляемое из поискового запроса
    if filters_request:
        user_filters_list = get_user_filters_request(filters_request)
    else:
        user_filters_list = []

    # обрабатываем поисковый запрос пользователя, номер выбранной страницы,
    # фильтры и передаем его в html

    if q and page_number and user_filters_list:
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
        watch_items = get_user_watch_list()
        title = 'Результаты поиска'
    elif q and user_filters_list:
        (results,
            total_pages,
            subcategory,
            subcategory_id,
            histogram_container_data) = find_items_advanced(
                q,
                chosen_categoryid,
                user_filters_list=user_filters_list,
                )
        watch_items = get_user_watch_list()
        page_number = 1
        title = 'Результаты поиска'
    elif q and page_number:
        (results,
            total_pages,
            subcategory,
            subcategory_id,
            histogram_container_data) = find_items_advanced(
                q,
                chosen_categoryid,
                page_number=page_number,
                )
        watch_items = get_user_watch_list()
        title = 'Результаты поиска'
    # обрабатываем начальный поисковый запрос пользователя без номера страницы
    # и передаем его в html
    elif q:
        (results,
            total_pages,
            subcategory,
            subcategory_id,
            histogram_container_data) = find_items_advanced(
                q,
                chosen_categoryid,
                )
        watch_items = get_user_watch_list()
        page_number = 1
        title = 'Результаты поиска'
    # параметры для передачи на страницу поиска без поискового запроса
    else:
        results = []
        title = None
        watch_items = []
        total_pages = ''
        page_number = ''
        subcategory = ''
        subcategory_id = ''
        histogram_container_data = ''

    return render_template(
        'ebay_search/search.html',
        title=title, results=results,
        categories=categories,
        totalpages=total_pages,
        watch_list=watch_items,
        pagenumber=page_number,
        subcategory=subcategory,
        subcategoryid=subcategory_id,
        histogram_container_data=histogram_container_data,
        userfilterslist=user_filters_list,
        )