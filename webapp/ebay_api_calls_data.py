from flask import current_app


headers = {
    "X-EBAY-API-CALL-NAME": "",
    "X-EBAY-API-DEV-NAME": current_app.config["DEVID"],
    "X-EBAY-API-APP-NAME": current_app.config["APPID"],
    "X-EBAY-API-CERT-NAME": current_app.config["CERTID"],
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

def getting_api_call_name(call_name):
    headers["X-EBAY-API-CALL-NAME"] = call_name
    return headers
