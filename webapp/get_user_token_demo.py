from bs4 import BeautifulSoup
from flask_login import current_user
import requests

import config
from ebay_api_calls_data import headers, getting_api_call_name
# from webapp import create_app
# from webapp.model import db, User

# Создание Session_ID для формирования ссылки передаваемой пользователю,
# для получения Token
def getting_session_ID():

    getting_api_call_name("GetSessionID")

    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GetSessionIDRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RuName>{config.RUNAME}</RuName>
    <Version>967</Version>
    </GetSessionIDRequest>
    """

    try:
        response = requests.post(
            url="https://api.ebay.com/ws/api.dll",
            headers=headers,
            data=data,
            )
    except requests.RequestException:
        return False

    response_soup = BeautifulSoup(response.content, "lxml")
    session_id = response_soup.find('sessionid').text

    # записываем session id в базу данных
    current_user.session_id = session_id
    current_user.session_id_status = True
    db.session.add(current_user)
    db.session.commit()

    return session_id



# Формирование ссылки, передаваемой пользователю, для получения Token
def getting_token_url():
    session_id = getting_session_ID()
    get_token_url = f"https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&runame={config.RUNAME}&SessID={session_id}"
    return get_token_url


# Получение Token после плучения согласия пользователя
def getting_token():
    
    if current_user.session_id_status: # проверяем имеется ли у текущего пользователя записанный в базе session_id
        session_id = current_user.session_id # получаем session id из баззы данных
        getting_api_call_name("FetchToken")

        data = f"""
        <?xml version="1.0" encoding="utf-8"?>
        <FetchTokenRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <Version>967</Version>
        <SessionID>{session_id}</SessionID>
        </FetchTokenRequest>
        """

        try:
            token_response = requests.post(
                url="https://api.ebay.com/ws/api.dll",
                headers=headers,
                data=data,
                )
        except requests.RequestException:
            return False
        
        token_respone_soup = BeautifulSoup(token_response.content, 'lxml')
        if token_respone_soup.find('ack').text == 'Success':
            token = token_respone_soup.find('ebayauthtoken').text
            return token
        else:
            return 'Пользователь не разрешил доступ'


def get_user_ebay_info(token)
""" На основании полученного Token - пользователя получаем его данные с """
headers = {
    "X-EBAY-API-CALL-NAME": "GetUser",
    "X-EBAY-API-DEV-NAME": "630211da-fe95-447d-8c74-5c8becda9b4b",
    "X-EBAY-API-APP-NAME": "Stanisla-khoshov-PRD-e69eabc60-e8608d88",
    "X-EBAY-API-CERT-NAME": "PRD-69eabc60f39c-8cbf-48b3-95f7-2932",
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
}

data = """
<?xml version="1.0" encoding="utf-8"?>
<GetUserRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**ElllXg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6MFkIujCpWEoQ+dj6x9nY+seQ**zzwGAA**AAMAAA**BT69wuOSTaa/DbiJ543iD8EDpPPA3tzEQQqRYUip9/bZSQvlf9wYt3w+51vJudaCKy/ieZqyFux/UIQRp8N+XQIHTtpctGxyse3TrfUVJ6bEfR+YvHhzZQI6qqCUgGnaDgEDFwKzYYRm9B47wnTARSdMYF5yKymuoSCPJ3eZkW/QTjgowZXOTfWQ35IK4vyQkYGO5g++YaCCfy3n3lA/s36+k8XuqUBVaYx0mB7sXW2ZFRw20IyeStHTC8LuZB5fybbK9QmmlhCOPXegxApxqwb/gOQKaj1HqCdK4gWVOHY2R3q6Q4S9hi7EHz19WPok45d56m7kIPs0NrILQ7tBTiqDstZaUghbE8WNf/6XIH9PABYNeTu7muQqIJCa2ltYIqaqkHzQbLz7xpH40v/Hxp5z9qDO9Mxz5tukHeCiX55JZYwzKjlepujrhwh92pXpJCwPxaiQcpslyPO70MdCfiWmoyjZXitvpKm1QmrnkXfFpz3e+gK6vr9hJ68u+pUExxIakfbZ4fWdpzFXqczgZsecWcYqQwYhSWn/ju+qy/OGZeAEX588KBMcDaiijHTxjyaW2rocQW5SR7VSOTJmxLuw9zJ559/PkIbi5zLmJd8B1rNFbpLFVSpy4lzNdEp/p8p0gV70+eNxUuc1SLtc7SDo/4BtcRcQqbN79RDFNVNA5aeije4BoTEHzbkgPnT5WT0eYzG8UbgEUbYoqbSi5SLxP/Hr7QSGGbABVqFih1dZsLNx57wtG/G3cWE1EYjC</eBayAuthToken>
  </RequesterCredentials> 
  <Version>967</Version>
</GetUserRequest>
"""

# r = requests.post(url="https://api.ebay.com/ws/api.dll", data=data, headers=headers)
# print(r.content)

# session_id = getting_session_ID()
# # session_id = "IDwGAA**e30c07a21700a4476006bd76fffffd81"

# print(getting_session_ID())
# # print(getting_token())