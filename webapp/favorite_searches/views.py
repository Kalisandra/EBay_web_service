import io
from datetime import datetime
from flask import Blueprint, request, render_template, Response
from flask_login import current_user
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from webapp import db
from webapp.favorite_searches.diagram_mpl import plot_statistics
from webapp.favorite_searches.models import Favorite_searches, Statistic_items
from webapp.user.decorators import user_required


blueprint = Blueprint(
    'favorite_searches', __name__, url_prefix='/favorite_searches')


@blueprint.route('/')
@user_required
def open_favorite_searches():
    favorite_searches_list = Favorite_searches.query.filter(
        Favorite_searches.user_id == current_user.id).order_by(
            Favorite_searches.date_of_creation.desc()).all()

    return render_template(
        'favorite_searches/favorite_searches.html',
        favorite_searches_list=favorite_searches_list
    )


@blueprint.route('/add_to_favorite_searches')
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
    # получаем имя сохраненного поискового запроса
    query_name = request.args.get('query_name')

    user_query_exists = Favorite_searches.query.filter(
        Favorite_searches.user_query == q).count()
    if not user_query_exists:
        new_user_query = Favorite_searches(
            user_id=current_user.id,
            query_name=query_name,
            user_query=q,
            chosen_categoryid=chosen_categoryid,
            filter_request=filters_request,
        )
        db.session.add(new_user_query)
        db.session.commit()

        return render_template(
            'favorite_searches/add_to_favorite_searches.html')


@blueprint.route('/remove_from_favorite_searches')
def remove_from_favorite_searches():
    search_id = request.args.get('id')
    if search_id:
        favorite_search = Favorite_searches.query.filter(
            Favorite_searches.id == search_id).first()
        db.session.delete(favorite_search)
        db.session.commit()
        title = "Поиск успешно удален из 'Избранных поисков'"
        return render_template(
            'favorite_searches/favorite_searches_action.html', title=title)


@blueprint.route('/add_statistic')
def add_statistic():
    search_id = request.args.get('id')
    if search_id:
        favorite_search = Favorite_searches.query.filter(
            Favorite_searches.id == search_id).first()
        favorite_search.statistic_status = True
        favorite_search.statistic_start_date = datetime.now()
        db.session.commit()
        title = "Сбор статистики цен включен"
        return render_template(
            'favorite_searches/favorite_searches_action.html', title=title)  


@blueprint.route('/stop_statistic')
def stop_statistic():
    search_id = request.args.get('id')
    if search_id:
        favorite_search = Favorite_searches.query.filter(
            Favorite_searches.id == search_id).first()
        favorite_search.statistic_status = False
        favorite_search.statistic_start_date = None
        db.session.commit()
        title = "Сбор статистики цен выключен"
        return render_template(
            'favorite_searches/favorite_searches_action.html', title=title)


@blueprint.route('/visualize_statistics')
def visualize_statistics():
    query_id = request.args.get('id')
    items_list = Statistic_items.query.filter(
        Statistic_items.query_id == query_id, Statistic_items.final_price.isnot(None)).order_by(Statistic_items.end_time.asc()).all()
    return render_template(
        'favorite_searches/visualize_statistics.html',
        items_list=items_list,
        query_id=query_id,
        )


@blueprint.route('/visualize_diagram')
def visualize_diagram():
    query_id = request.args.get('id')
    diagram = plot_statistics(query_id)
    output = io.BytesIO()
    diagram = FigureCanvas(diagram).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
