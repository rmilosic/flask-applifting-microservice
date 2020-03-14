import pytest
import random
import uuid

from flask import session

from app import functions
from app.models import Product


def test_get_auth_token(client):
    """Test if authorisation token is being retrieved"""
    rv = client.get('products')
    access_token = functions.get_auth_token()
    assert isinstance(access_token, str)

def test_set_access_token(client):
    """Test if authorisation token is being set"""
    rv = client.get('/products')
    assert session.get("OFFER_ACCESS_TOKEN") == None
    functions.set_access_token()
    assert isinstance(session["OFFER_ACCESS_TOKEN"], str)

def test_register_product(client):
    """Test if product is successfully registered"""
    rv = client.get('/products')
    id = uuid.uuid1()
    product = Product(
        id=id,
        name="test_1",
        description="test_1"
    )
    response = functions.register_product(product)

    assert response.status_code == 201
    assert response.json().get('id') == str(product.id)
    
