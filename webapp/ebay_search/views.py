from flask import Blueprint, flash, render_template, request

from webapp.ebay_search.find_items import (
    find_items_advanced, add_to_watch_list,
)
from webapp.ebay_search.models import Ebay_Categories


blueprint = Blueprint('search', __name__, url_prefix='/search')

@blueprint.route('/')
def search():
    # получаем категории товаров Ebay из базы данных 
    categories = Ebay_Categories.query.filter(Ebay_Categories.categorylevel == 1)
    # получаем результаты запроса от пользователя 
    q = request.args.get('q') #поисковая строка
    chosen_categoryid = request.args.get('categoryid') # выбранная категория

    # обрабатываем поисковый запрос пользователя и передаем его в html
    if q:
        results = find_items_advanced(q, chosen_categoryid)
        title = 'Результаты поиска'
    else:
        results = None
        title = None
        flash('Выберите категорию поиска')
    
    return render_template('ebay_search/search.html', title=title, results=results, categories=categories)

@blueprint.route('/add_to_watch_list')
def add_to():
    item_id = request.args.get('itemid')
    if item_id:
        add_to_watch_list(item_id)

        return render_template('ebay_search/add_to_watch_list.html')





