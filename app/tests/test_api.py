import pytest
import random
import uuid
import logging

from flask import session

from app import functions
from app.models import Product, Offer

logger = logging.Logger(__name__, level=logging.INFO)

def test_get_products(client):
    """
    Test getting an empty product list
    """
    response = client.get('/products')
    
    assert response.status_code == 200
    assert response.json == []


def test_post_product(client):
    """
    Test creation of a product
    """
    response = client.post('/products', data={"name": "Test product", "description": "Empty field"})

    assert response.status_code == 201
    assert response.json["name"] == "Test product"


def test_get_single_product(client):
    """
    Test get a single product after creation
    """
    res_post = client.post('/products', data={"name": "Test product", "description": "Empty field"})
    
    product_id = res_post.json["id"]
    get_link = "/products/" + str(product_id)
    
    res_get_specific_product = client.get(get_link)
    
    assert res_get_specific_product.status_code == 200
    
    
def test_update_single_product(client):
    """
    Test updating a created product
    """
    new_name = "Updated name"
    
    res_post_create = client.post('/products', data={"name": "Test product", "description": "Empty field"})
    product_id = res_post_create.json["id"]

    res_post_update = client.put(f"/products/{str(product_id)}", data={"name": new_name, "description": ""})

    product_name_updated = res_post_update.json["name"]
    
    assert res_post_update.status_code == 201
    assert product_name_updated == new_name


def test_delete_single_product(client):
    """
    Test deleting a created product
    """
    res_post_create = client.post('/products', data={"name": "Test product", "description": "Empty field"})
    product_id = res_post_create.json["id"]

    res_post_delete = client.delete(f"/products/{str(product_id)}")

    assert res_post_delete.status_code == 204
