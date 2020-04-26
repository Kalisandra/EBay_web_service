from flask import Blueprint, render_template

from webapp.ebay_search.get_category import get_ebay_categories
from webapp.ebay_search.find_items import get_user_watch_list
from webapp.user.decorators import admin_required
from webapp.favorite_searches.diagram_mpl import plot_statistics
from webapp.favorite_searches.statistic import get_final_price


blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required
def admin_index():
    plot_statistics(4)
    title = "Панель управления"
    return render_template('admin/index.html', page_title=title)