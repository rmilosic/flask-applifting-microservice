import os
import requests
from datetime import datetime

from flask import session
from flask import current_app

from app import db
from app.models import Product, Offer

from . import celery

offer_microservice_token_name = 'OFFER_ACCESS_TOKEN'

def register_product(product: Product) -> str:
    """Register a product with offer microservice"""   

    # get a new access token if not set
    access_token = get_or_set_access_token(
        token_name=offer_microservice_token_name,
        get_token_func=get_offer_microservice_auth_token
        )
        
    base_url = os.environ["OFFERS_MICROSERVICE_BASE_URL"]
    register_url = base_url+'/products/register'
    headers = {
        "Bearer": access_token
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
    
def get_offer_microservice_auth_token():
    base_url = os.environ['OFFERS_MICROSERVICE_BASE_URL']
    response_json = requests.post(base_url+'/auth').json()
    access_token = response_json["access_token"]
    current_app.logger.info(f"retrieved access token {access_token}")
    return access_token

def set_access_token(token_name: str, get_token_func: callable):
    """Sets a new access token"""
    # base url of microsevices and appended
    access_token = get_offer_microservice_auth_token()
    session[token_name] = access_token
    current_app.logger.info(f"set access token {session.get(token_name)}")

def get_or_set_access_token(token_name: str, get_token_func: callable):
    """Get or set access token"""
    if not session.get(token_name):
        set_access_token(token_name, get_token_func)

    return session.get(token_name)

def call_offers_microservice(product_id: str) -> dict:
    """Call offer microservice"""
    base_url = os.environ["OFFERS_MICROSERVICE_BASE_URL"]
    offer_service_url = base_url+'/products/{id}/offers'.format(id=product_id)
    
    access_token = get_or_set_access_token(
        token_name=offer_microservice_token_name,
        get_token_func=get_offer_microservice_auth_token
        )
    
    response = requests.get(
        url=offer_service_url,
        headers={
            "Bearer": access_token
        }
    )

    return response


@celery.task
def refresh_offer_prices():  
    started = datetime.now()  
    # products in scope (non-deleted)
    products = Product.query.filter(Product.deleted==None).all()
    
    offers_no = 0
    products_no = 0
    # loop through non-deleted products 
    for product in products:
    
        # call offer microservice with correct product id
        response = call_offers_microservice(str(product.id))
        if response.status_code == 200:
            offer_list = response.json()
        else:
            current_app.logger.info(f"Offers response for product id {product.id}: {response}")
            continue
        
        # loop found offers items and save to db 
        for offer_item in offer_list:
            current_app.logger.info(f"Offer example {offer_item}")
            offer = Offer(
                seller_id=offer_item.get("id"),
                price=offer_item.get("price"),
                items_in_stock=offer_item.get("items_in_stock"),
                product_id=product.id
            )
            db.session.add(offer)
            db.session.commit()

            offers_no += 1
        
        products_no += 1
    
    finished = datetime.now()
        
    return {
        "code": "OK",
        "message": f"Processed {offers_no} offers for {products_no} products",
        "started": started,
        "finished": finished
    }
