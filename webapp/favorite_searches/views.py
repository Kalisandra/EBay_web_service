from datetime import datetime
from flask import Blueprint, request
from flask_login import current_user

from webapp import db
from webapp.favorite_searches.models import Favorite_searches
from webapp.user.decorators import user_required


blueprint = Blueprint('favorite_searches', __name__, url_prefix='/favorite_searches')

@blueprint.route('/')
@user_required
def add_to_favorite_searches():
    """
    Функция добавляет поиск в базу данных "Избранные поиски"
    """
    # получаем результаты запроса от пользователя из поисковой строки
    q = request.args.get('q')
    # получаем выбранную категорию со страницы поиска
    chosen_categoryid = request.args.get('categoryid')
    # получаем значения выбранных фильтров расширенного поиска
    filters_request = request.args.get('filters')

    user_query_exists = Favorite_searches.query.filter(
        Favorite_searches.user_query == q).count()
    if not user_query_exists:
        new_user_query_exists = Favorite_searches(
            user_id=current_user.user_id,
            user_query=q,
            chosen_categoryid=chosen_categoryid,
            filters_request=filters_request,
            date_of_creation=datetime.now()
            )
        db.session.add(new_user_query_exists)
        db.session.commit()