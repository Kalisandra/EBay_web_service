from flask import current_app
import requests


def get_session_ID():
    headers = {
        "X-EBAY-API-CALL-NAME": "GetSessionID",
        "X-EBAY-API-DEV-NAME": current_app.config['DEVID'],
        "X-EBAY-API-APP-NAME": current_app.config['APPID '],
        "X-EBAY-API-CERT-NAME": current_app.config['CERTID'],
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "Content-Type": "text/xml"
    }

    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GetSessionIDRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RuName>{current_app.config['RUNAME']}</RuName>
    <Version>967</Version>
    </GetSessionIDRequest>
    """

    r = requests.post(url="https://api.ebay.com/ws/api.dll", data=data, headers=headers)

print(r.content)