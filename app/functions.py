import os
import requests

from flask import session
from flask import current_app
from app.models import Product

def register_product(product: Product) -> str:
    """Register a product with offer microservice"""   

    # get a new access token if not set
    if not session.get('OFFER_ACCESS_TOKEN'):
        set_access_token()
        
    base_url = os.environ["OFFERS_MICROSERVICE_BASE_URL"]
    register_url = base_url+'/products/register'
    headers = {
        "Bearer": session.get('OFFER_ACCESS_TOKEN')
    }
    current_app.logger.info(f"Headers: {headers}")
    response = requests.post(
        register_url,
        data={
            "id": str(product.id),
            "name": product.name,
            "description": product.description
        },
        headers=headers)
    current_app.logger.info(response)
    return response
    
def get_auth_token():
    base_url = os.environ['OFFERS_MICROSERVICE_BASE_URL']
    response_json = requests.post(base_url+'/auth').json()
    access_token = response_json["access_token"]
    current_app.logger.info(f"retrieved access token {access_token}")
    return access_token

def set_access_token():
    """Sets a new access token"""
    # base url of microsevices and appended
    access_token = get_auth_token()
    session["OFFER_ACCESS_TOKEN"] = access_token
    current_app.logger.info(f"set access token {session.get('OFFER_ACCESS_TOKEN')}")



