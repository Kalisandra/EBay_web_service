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


    # def search_data_request(filters, categiryid, query, page_number):
    # if not filters:
    #     data = f"""
    #     <findItemsAdvancedRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
    #     <categoryId>{categiryid}</categoryId>
    #     <outputSelector>AspectHistogram</outputSelector>
    #     <descriptionSearch>true</descriptionSearch>
    #     <keywords>{query}</keywords>
    #     <itemFilter>
    #         <name>ListingType</name>
    #         <value>Auction</value>
    #         <value>AuctionWithBIN</value>
    #     </itemFilter>
    #     <paginationInput>
    #         <entriesPerPage>50</entriesPerPage>
    #         <pageNumber>{page_number}</pageNumber>
    #     </paginationInput>
    #     <sortOrder>EndTimeSoonest</sortOrder>
    #     </findItemsAdvancedRequest>"""
    # else:
    
    #     data = f"""
    #     <findItemsAdvancedRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
    #     <categoryId>{categiryid}</categoryId>
    #     <outputSelector>AspectHistogram</outputSelector>
    #     <descriptionSearch>true</descriptionSearch>
    #     <keywords>{query}</keywords>
    #     <itemFilter>
    #         <name>ListingType</name>
    #         <value>Auction</value>
    #         <value>AuctionWithBIN</value>
    #         {filters}
    #     </itemFilter>
    #     <paginationInput>
    #         <entriesPerPage>50</entriesPerPage>
    #         <pageNumber>{page_number}</pageNumber>
    #     </paginationInput>
    #     <sortOrder>EndTimeSoonest</sortOrder>
    #     </findItemsAdvancedRequest>"""


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