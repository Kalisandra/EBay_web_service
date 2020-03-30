from flask import Blueprint, render_template, request

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
    item_id = request.args.get('itemid')
    if item_id:
        add_to_watch_list(item_id)

    # обрабатываем поисковый запрос пользователя и передаем его в html
    if q:
        results = find_items_advanced(q, chosen_categoryid)
    else:
        results = None
    
    return render_template('ebay_search/search.html', results=results, categories=categories)




