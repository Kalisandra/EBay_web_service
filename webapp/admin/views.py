from flask import Blueprint, render_template

from webapp.ebay_search.get_category import get_ebay_categories
from webapp.user.decorators import admin_required


blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = "Панель управления"
    return render_template('admin/index.html', page_title=title)
