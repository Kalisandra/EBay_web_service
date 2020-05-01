from flask import Blueprint, render_template

from webapp.user.decorators import admin_required
from webapp.ebay_search.get_category import get_ebay_categories

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    get_ebay_categories()
    title = "Панель управления"
    return render_template('admin/index.html', page_title=title)
