import pytest
import random
import uuid

from flask import session

from app import functions
from app.models import Product, Offer


def test_get_or_set_access_token(client):
    """Test if authorisation token is being retrieved"""
    rv = client.get('products')
    token_name = 'TEST_TOKEN'
    access_token = functions.get_or_set_access_token(
        token_name,
        functions.get_offer_microservice_auth_token
    )
    assert isinstance(access_token, str)

def test_set_access_token(client):
    """Test if authorisation token is being set"""
    rv = client.get('/products')
    token_name = 'TEST_TOKEN'
    assert session.get(token_name) == None
    functions.set_access_token(
        token_name,
        functions.get_offer_microservice_auth_token
    )
    assert isinstance(session[token_name], str)

def test_register_product(client):
    """Test if product is successfully registered"""
    client.get('/products')
    id = uuid.uuid1()
    product = Product(
        id=id,
        name="test_1",
        description="test_1"
    )
    response = functions.register_product(product)

    assert response.status_code == 201
    assert response.json().get('id') == str(product.id)

def test_refresh_offer_prices(client):
    """Test if function finishes execution"""
    rv = client.get('/products')
    response = functions.refresh_offer_prices()
    assert response["code"] == "OK"
   

def test_call_offers_microservice(client):
    """Test API call to offers microservice"""
    rv = client.get('/products')
    product_id = '1'
    response = functions.call_offers_microservice(product_id)
    assert response.status_code == 200