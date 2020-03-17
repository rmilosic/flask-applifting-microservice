from datetime import datetime
import uuid
import os
import requests
from datetime import datetime
from typing import Union

from flask import session
from flask import current_app

from app import db

from app.models import Product, Offer

offer_microservice_token_name = 'OFFER_ACCESS_TOKEN'

def refresh_offer_prices() -> dict:
    """
    Celery task for retrieving offers and their prices for 
    individual products
    """
    started = datetime.now()  
    # products in scope (non-deleted)
   
    products = Product.query.filter(Product.deleted==None).all()
    
    
    # loop through non-deleted products 
    for product in products:

        # call offer microservice with correct product id
        response = call_offers_microservice(str(product.id))
        
        
        if response.status_code == 200:
            offer_list = response.json()
        else:
            # current_app.logger.info(f"Offer response with status code: {response.status_code}")
            continue
        
        # loop found offers items and save to db 
        for offer_item in offer_list:
            offer = Offer(
                seller_id=offer_item.get("id"),
                price=offer_item.get("price"),
                items_in_stock=offer_item.get("items_in_stock"),
                product_id=product.id
            )
            db.session.add(offer)
            db.session.commit()

            # current_app.logger.info(f"Saved {len(offer_list)} for item id: {product.id}")
        
        
    return {
        "code": "OK",
        "message": "Successfuly saved offers",
        "started": started,
        "finished": datetime.now()
    }


def register_product(product: Product) -> str:
    """
    Register a product with offer microservice
    """   
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
    # current_app.logger.info(f"Headers: {headers}")
    response = requests.post(
        register_url,
        data={
            "id": str(product.id),
            "name": product.name,
            "description": product.description
        },
        headers=headers)
    # current_app.logger.info(response)
    return response
    
def get_offer_microservice_auth_token() -> str:
    """
    Gets an access token from the offer microservice
    """
    base_url = os.environ['OFFERS_MICROSERVICE_BASE_URL']
    response_json = requests.post(base_url+'/auth').json()
    access_token = response_json["access_token"]
    # current_app.logger.info(f"retrieved access token {access_token}")
    return access_token

def set_access_token(token_name: str, get_token_func: callable) -> None:
    """
    Sets a new access token
    """
    # base url of microsevices and appended
    access_token = get_offer_microservice_auth_token()
    session[token_name] = access_token
    # current_app.logger.info(f"set access token {session.get(token_name)}")

def get_or_set_access_token(token_name: str, get_token_func: callable) -> str:
    """
    Get or set access token
    """
    if not session.get(token_name):
        set_access_token(token_name, get_token_func)

    return session.get(token_name)

def call_offers_microservice(product_id: str) -> requests.Response:
    """
    Call offer microservice
    """
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



def validate_uuid4(uuid_string: Union[uuid.UUID, str]) -> bool:
    """
    Validate that a UUID string is in
    fact a valid uuid4.
    Happily, the uuid module does the actual
    checking for us.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    if not isinstance(uuid_string, uuid.UUID):
        try:
            val = uuid.UUID(uuid_string, version=4)
        except ValueError:
            # If it's a value error, then the string 
            # is not a valid hex code for a UUID.
            return False
    else:
        return True

    # If the uuid_string is a valid hex code, 
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a 
    # valid uuid4. This is bad for validation purposes.

    return str(val) == uuid_string