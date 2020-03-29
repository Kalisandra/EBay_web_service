from datetime import datetime

from bs4 import BeautifulSoup
from flask import current_app
from flask_login import current_user
import requests


from webapp.user.models import db, User
from webapp.utils import get_shopping_headers, post_ebay_request


# Создание Session_ID для формирования ссылки передаваемой пользователю,
# для получения Token
def get_session_ID():

    headers = get_shopping_headers("GetSessionID")

    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GetSessionIDRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RuName>{current_app.config['RUNAME']}</RuName>
    <Version>967</Version>
    </GetSessionIDRequest>
    """

    response_soup = post_ebay_request(headers, data)
    session_id = response_soup.find('sessionid').text

    # записываем session id в базу данных

    current_user.session_id = session_id
    current_user.session_id_status = True
    db.session.add(current_user)
    db.session.commit()

    return session_id




def get_token_url():
    """Формирование ссылки, передаваемой пользователю, для получения Token"""
    session_id = get_session_ID()
    token_url = f"https://signin.ebay.com/ws/eBayISAPI.dll?SignIn\
        &runame={current_app.config['RUNAME']}&SessID={session_id}"
    return token_url


def get_token():
    """Запрос Token после плучения согласия пользователя"""
    if current_user.session_id_status: # проверяем имеется ли у текущего пользователя записанный в базе session_id
        session_id = current_user.session_id # получаем session id из баззы данных
        headers = get_shopping_headers("FetchToken")

        data = f"""
        <?xml version="1.0" encoding="utf-8"?>
        <FetchTokenRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <Version>967</Version>
        <SessionID>{session_id}</SessionID>
        </FetchTokenRequest>
        """
        
        response_soup = post_ebay_request(headers, data)
        if response_soup.find('ack').text == 'Success':
            token = response_soup.find('ebayauthtoken').text
            hard_expiration_time = response_soup.find('hardexpirationtime').text
            # удаляем ненужные символы из 'hard_expiration_time'
            hard_expiration_time = hard_expiration_time.replace('T', ' ').replace('Z', '')
            # преобразуем строку 'hard_expiration_time' в datetime
            hard_expiration_time = datetime.strptime(hard_expiration_time, '%Y-%m-%d %H:%M:%S.%f')

            # записываем полученные данные в базу
            current_user.token = token
            current_user.hard_expiration_time = hard_expiration_time
            # проверяем статус токена на текущу дату
            if hard_expiration_time > datetime.now(tz=None):
                current_user.token_status = True
            else:
                current_user.token_status = False
            db.session.add(current_user)
            db.session.commit()

        else:
            return 'Пользователь не разрешил доступ'

