import requests
from bs4 import BeautifulSoup
from flask_login import current_user
from webapp.utils import get_shopping_headers, post_ebay_request

# def get_item():
#     headers = {
#         "Authorization": "Bearer v^1.1#i^1#f^0#p^1#r^0#I^3#t^H4sIAAAAAAAAAOVYb2wURRTvtdc2BIuYECwE47EFSSS7N7u3t93bcgdHW+BsoaV3FFrEsrc7W5buP3b2aM9GaPoBPhAIH6SCgVA1ajQhpIgxEmPQIKEY4YOgiBIkRGggJGoENZHo7vYo10rKn16kifflMm/evPm933tv5u2ArqIJz29ZsuX3Ek9xfm8X6Mr3eMiJYEJR4dxJBfnTC/NAloKnt2tWl7e7YGAe4lXF4BogMnQNQV+HqmiIc4VhLGVqnM4jGXEar0LEWQIXjy6t5SgCcIapW7qgK5gvVhXGGIokAwwTSopCkoEBypZqd2wm9DBGMpCWeCAEqQAdospFex6hFIxpyOI1K4xRgAI4oHHAJMgQR5McoIkgCDVjvkZoIlnXbBUCYBEXLueuNbOwjg6VRwialm0Ei8Sii+J10VhV9bLEPH+WrUiGh7jFWyk0fFSpi9DXyCspOPo2yNXm4ilBgAhh/sjgDsONctE7YB4Bvku1GGIDkkiV06QEgBTgc0LlIt1UeWt0HI5EFnHJVeWgZslW+n6M2mwk10PByoyW2SZiVT7nb3mKV2RJhmYYq14YbYrW12ORqCaaUK7h8cUp1WCDeH1DFU4zIcgnBQbgEsWWM4Apz2wzaCtD8oh9KnVNlB3KkG+Zbi2ENmY4kplAFjO2Up1WZ0Yly8GTpUeRQwzSzU5IB2OYstZpTlShatPgc4f3539otWWZcjJlwSELIydcgsIYbxiyiI2cdDMxkzwdKIytsyyD8/vb29uJ9gChm61+CgDSv2ppbVxYB1U7Pxxdp9Ydffn+C3DZdUWA9kokc1basLF02JlqA9BasQgNWAawGd6Hw4qMlP5LkOWzf3g95Ko+JJYsDwVIyAJKZFiJykV9RDIp6ndwwCSfxlXebIOWofACxAU7z1IqNGWRCwQlKsBKEBeZkITTIUnCk0GRwUkJQgBhMimE2P9PmTxoosehYEIrR5meoyyvVY2OmkVNC/l0TWNofWWrlpTTyYblCclsRhtWNvvnomBDbVIDq+Sl4QethXs7L+gGrNcVWUiPv1oPmGI9b1rpOFQUWzAmR5Hj6PgKsrMe2QZ4QyacsiYEXfXrvH2eO6IWF/GYfI4aRkxVUxafVGAsV2f5YznH7+mebPc548onO36DgZTFwQaFcKNJoI0CYUKkp0y7NyPqnBs7obdBzT4BLVNXFGg2kmMO9OOIr1Pro/DxUFfFo3meyy5l/GS2oMh2ArWMN8/+g3jK/Di7ickgyzi9BkOPya9KN6KJ9Hi7g5boyILig7jmnf+QDbV/+Md9JM/9kd2eD0G3py/f4wF+MJssAzOLClZ4C56YjmQLEjIvEUhu1exvVhMSbTBt8LKZX+QxVvDXZmc9J/SuAaVDDwoTCsiJWa8LYMbdmULyyadLbEpowJAhmrQbRFB2d9ZLTvVOOfHp5FkzA0cXv7Fz65fFm2+17tm3aj8oGVLyeArzvN2ePN+JmwPtgvDigZPHL/corx9/bkH1ue1mE/rlq00DhT+fead221pm7oGSOW/t/myH2jnw3eJPysAkWjN6ZhT3X5h5afWhHmHq99uOx9jels76jlL5vc6+86v/VK/e/PXiwbI3b50WP/9j2t6rNf19Z9o3H9y/e98re7+pKKB/OvbRb+noRWnNYU/P5u5j6dtdiT6v/1pN/tofdr3UXzu/LME1fXzl1KFJX1fcviErZ658sLL4mZ2b3n1t7/ID10tLv2C5yzv+XvLsjbYjC072ExsrWm5PO7V715TVYvWFv65f3m+pp/eUP/V2YMalI60bvj3fdvjljqLJc9it285VnE1V9Z49+uP7L8ReJVO3tncOhu8fqP/pWegRAAA=",
#         "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
#         "Content-Type": "application/json",
#     }

#     response = requests.get(
#         url="https://api.ebay.com/buy/browse/v1/item/v1|184233431247|0",
#         headers=headers,
#         )
#     print(response.status_code)
#     response = response.json()

#     print(response)
#     return response

# def make_offer():
#     headers = {
#         "Authorization": "Bearer v^1.1#i^1#f^0#p^1#r^0#I^3#t^H4sIAAAAAAAAAOVYb2wURRTvtdc2BIuYECwE47EFSSS7N7u3t93bcgdHW+BsoaV3FFrEsrc7W5buP3b2aM9GaPoBPhAIH6SCgVA1ajQhpIgxEmPQIKEY4YOgiBIkRGggJGoENZHo7vYo10rKn16kifflMm/evPm933tv5u2ArqIJz29ZsuX3Ek9xfm8X6Mr3eMiJYEJR4dxJBfnTC/NAloKnt2tWl7e7YGAe4lXF4BogMnQNQV+HqmiIc4VhLGVqnM4jGXEar0LEWQIXjy6t5SgCcIapW7qgK5gvVhXGGIokAwwTSopCkoEBypZqd2wm9DBGMpCWeCAEqQAdospFex6hFIxpyOI1K4xRgAI4oHHAJMgQR5McoIkgCDVjvkZoIlnXbBUCYBEXLueuNbOwjg6VRwialm0Ei8Sii+J10VhV9bLEPH+WrUiGh7jFWyk0fFSpi9DXyCspOPo2yNXm4ilBgAhh/sjgDsONctE7YB4Bvku1GGIDkkiV06QEgBTgc0LlIt1UeWt0HI5EFnHJVeWgZslW+n6M2mwk10PByoyW2SZiVT7nb3mKV2RJhmYYq14YbYrW12ORqCaaUK7h8cUp1WCDeH1DFU4zIcgnBQbgEsWWM4Apz2wzaCtD8oh9KnVNlB3KkG+Zbi2ENmY4kplAFjO2Up1WZ0Yly8GTpUeRQwzSzU5IB2OYstZpTlShatPgc4f3539otWWZcjJlwSELIydcgsIYbxiyiI2cdDMxkzwdKIytsyyD8/vb29uJ9gChm61+CgDSv2ppbVxYB1U7Pxxdp9Ydffn+C3DZdUWA9kokc1basLF02JlqA9BasQgNWAawGd6Hw4qMlP5LkOWzf3g95Ko+JJYsDwVIyAJKZFiJykV9RDIp6ndwwCSfxlXebIOWofACxAU7z1IqNGWRCwQlKsBKEBeZkITTIUnCk0GRwUkJQgBhMimE2P9PmTxoosehYEIrR5meoyyvVY2OmkVNC/l0TWNofWWrlpTTyYblCclsRhtWNvvnomBDbVIDq+Sl4QethXs7L+gGrNcVWUiPv1oPmGI9b1rpOFQUWzAmR5Hj6PgKsrMe2QZ4QyacsiYEXfXrvH2eO6IWF/GYfI4aRkxVUxafVGAsV2f5YznH7+mebPc548onO36DgZTFwQaFcKNJoI0CYUKkp0y7NyPqnBs7obdBzT4BLVNXFGg2kmMO9OOIr1Pro/DxUFfFo3meyy5l/GS2oMh2ArWMN8/+g3jK/Di7ickgyzi9BkOPya9KN6KJ9Hi7g5boyILig7jmnf+QDbV/+Md9JM/9kd2eD0G3py/f4wF+MJssAzOLClZ4C56YjmQLEjIvEUhu1exvVhMSbTBt8LKZX+QxVvDXZmc9J/SuAaVDDwoTCsiJWa8LYMbdmULyyadLbEpowJAhmrQbRFB2d9ZLTvVOOfHp5FkzA0cXv7Fz65fFm2+17tm3aj8oGVLyeArzvN2ePN+JmwPtgvDigZPHL/corx9/bkH1ue1mE/rlq00DhT+fead221pm7oGSOW/t/myH2jnw3eJPysAkWjN6ZhT3X5h5afWhHmHq99uOx9jels76jlL5vc6+86v/VK/e/PXiwbI3b50WP/9j2t6rNf19Z9o3H9y/e98re7+pKKB/OvbRb+noRWnNYU/P5u5j6dtdiT6v/1pN/tofdr3UXzu/LME1fXzl1KFJX1fcviErZ658sLL4mZ2b3n1t7/ID10tLv2C5yzv+XvLsjbYjC072ExsrWm5PO7V715TVYvWFv65f3m+pp/eUP/V2YMalI60bvj3fdvjljqLJc9it285VnE1V9Z49+uP7L8ReJVO3tncOhu8fqP/pWegRAAA=",
#         "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "maxAmount": {
#             "currency": "USD",
#             "value": "17.50",
#         }
#     }

#     response = requests.post(
#         url="https://api.ebay.com/buy/offer/v1_beta/bidding/v1|184233431247|0/place_proxy_bid",
#         headers=headers,
#         json=data
#         )
    
#     print(response.status_code)
#     response = response.json()

#     print(response)
#     return response

# def user_filters_request(filters_request):
#     filters_data = filters_request.split(';')
#     filters_data.remove(filters_data[-1])
#     user_filters_request = []
#     for filters in filters_data:
#         category_filters = {}
#         one_category_filters = filters.split(':')
#         category_filters['filter_name'] = one_category_filters[0]
#         category_filters['filter_values'] = one_category_filters[1].split(',')
#         user_filters_request.append(category_filters)
#     return user_filters_request

# def make_filter_string_for_finding_request(user_filters_request):
#     test_string = ''
#     for filters in user_filters_request:
#         if not len(test_string):
#             test_string += f"<name>{filters['filter_name']}</name>"
#         else:
#             test_string += '\n' + f"<name>{filters['filter_name']}</name>"
#         for value in filters['filter_values']:
#             test_string += '\n' + f"<value>{value}</value>"

user_string = 'Binding:Hardcover;Subject:Biography & Autobiography;'

def get_item():
    headers = get_shopping_headers("GetItem")
    token = current_user.token
    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{token}</eBayAuthToken>
    </RequesterCredentials>
    <ItemID>264684789864</ItemID>
    </GetItemRequest>"""

    response_soup = post_ebay_request(headers, data)
    item = response_soup.find('item')
    pars_item = {}
    for key, value in soup_keys.items():
        pars_item[key] = parsfield(item, value)

    return pars_item
