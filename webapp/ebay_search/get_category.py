from flask_login import current_user

from webapp.utils import get_shopping_headers, post_ebay_request
from webapp.ebay_search.models import Ebay_Categories

def get_ebay_categories():
    """Запрос категорий с Ebay"""

    headers = get_shopping_headers("GetCategories")
    token = current_user.token
    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GetCategoriesRequest xmlns= >
        <RequesterCredentials>
            <eBayAuthToken>{token}</eBayAuthToken>
        </RequesterCredentials> 
        <CategorySiteID>0</CategorySiteID>
    <DetailLevel>ReturnAll</DetailLevel>
    <LevelLimit>2</LevelLimit>
    </GetCategoriesRequest>
    """

    response_soup = post_ebay_request(headers, data)
    all_categories = response_soup.findAll('category')
    for category in all_categories:
        category_level = category.find('categorylevel').text
        category_name = category.find('categoryname').text
        category_id = category.find('categoryid').text
        category_parent_id = category.find('categoryparentid').text
        # print(f'level = {category_level}, name = {category_name}, id = {category_id}, parent_id = {category_parent_id}')
        save_category(
            category_name,
            category_level,
            category_id,
            category_parent_id,
            )



def save_category(categoryname, categorylevel, categoryid, categoryparentid):
    """Функция записи категорий в базу данных"""

    category_exists = Ebay_Categories.query.filter(
        Ebay_Categories.categoryid == categoryid).count()
    if not category_exists:
        new_category = Ebay_Categories(
            categoryname=categoryname,
            categorylevel=categorylevel,
            categoryid=categoryid,
            categoryparentid=categoryparentid,
            )
    db.session.add(new_category)
    db.session.commit()