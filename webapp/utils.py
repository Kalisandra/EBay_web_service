from bs4 import BeautifulSoup
from flask import current_app
import requests


def get_shopping_headers(call_name):
    """Создаем headers для направления shopping запроса на api.ebay.
    В качестве аргумента передаем название запроса
    """
    headers = {
        "X-EBAY-API-CALL-NAME": call_name,
        "X-EBAY-API-DEV-NAME": current_app.config["DEVID"],
        "X-EBAY-API-APP-NAME": current_app.config["APPID"],
        "X-EBAY-API-CERT-NAME": current_app.config["CERTID"],
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "Content-Type": "text/xml"
    }
    return headers


def get_finding_headers(call_name):
    """Создаем finding headers для направления HTTPS запроса на 
    https://svcs.ebay.com/services/search/FindingService/v1
    В качестве аргумента передаем название запроса
    """
    headers = {
        "X-EBAY-SOA-SERVICE-NAME": "FindingService",
        "X-EBAY-SOA-OPERATION-NAME": call_name,
        "X-EBAY-SOA-GLOBAL-ID": "EBAY-US",
        "X-EBAY-SOA-SECURITY-APPNAME": current_app.config["APPID"],
    }
    return headers


def post_ebay_request(headers, data):
    """Направление запроса на api.ebay методом POST.
    В качестве аргументов передаем headers и data
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
    return response_soup

def post_ebay_finding_request(headers, data):
    """Направление запроса на https://svcs.ebay.com/services/search/FindingService/v1 
    методом POST. В качестве аргументов передаем headers и data
    """ 
    try:
        response = requests.post(
        url="https://svcs.ebay.com/services/search/FindingService/v1",
        headers=headers,
        data=data,
        )
    except requests.RequestException:
        return False

    response_soup = BeautifulSoup(response.content, "lxml")
    return response_soup