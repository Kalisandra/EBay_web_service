from flask import Blueprint, flash, render_template, request

from webapp.ebay_search.find_items import (
    find_items_advanced, add_to_watch_list, get_user_watch_list, remove_from_user_watch_list
)
from webapp.ebay_search.models import Ebay_Categories
from webapp.user.decorators import user_required


blueprint = Blueprint('search', __name__, url_prefix='/search')

@blueprint.route('/')
@user_required
def search():
    # получаем категории товаров Ebay из базы данных 
    categories = Ebay_Categories.query.filter(Ebay_Categories.categorylevel == 1)
    # получаем результаты запроса от пользователя 
    q = request.args.get('q') #поисковая строка
    chosen_categoryid = request.args.get('categoryid') # выбранная категория

    # обрабатываем поисковый запрос пользователя и передаем его в html
    if q:
        results = find_items_advanced(q, chosen_categoryid)
        watch_items = get_user_watch_list()
        title = 'Результаты поиска'
    else:
        results = []
        title = None
        watch_items = []
        flash('Выберите категорию поиска')

    return render_template('ebay_search/search.html', title=title, results=results, categories=categories, watch_list=watch_items)

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
    return render_template('ebay_search/watch_list.html', watch_list=watch_items)

@blueprint.route('/remove_item')
def remove_from():
    item_id = request.args.get('itemid')
    if item_id:
        remove_from_user_watch_list(item_id)

        return render_template('ebay_search/remove_from_watch_list.html')
