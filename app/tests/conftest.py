import os
import tempfile
import pytest
 
from flask import current_app

from app import create_app, db
from app.models import Product, Offer


@pytest.fixture
def client():
    app = create_app()
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Establish an application context before running the tests.
    with app.test_client() as client:
        
        yield client


@pytest.fixture()
def new_product():
    product = Product(name="Test product", description="testing is cool")
    return product
 

    

