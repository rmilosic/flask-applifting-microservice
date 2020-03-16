import pytest
import random
import uuid

from flask import session

from app import functions
from app.models import Product, Offer


def test_get_products(client):
    """Test get product list"""
    response = client.get('/products')
    
    assert response.status_code == 200
    assert response.json == []


def test_post_product(client):
    response = client.post('/products', data={"name": "Test product", "description": "Empty field"})

    assert response.status_code == 201
    assert response.data["name"] == "Test product"


def test_get_single_product(client):
    """Test get product list"""
    res = client.post('/products', data={"name": "Test product", "description": "Empty field"})
    res = client.get('/products')
    product = res.data[0]
    
    res = client.get(f'/products/{product.get("id")}')
    
    assert res.status_code == 200
    
    
