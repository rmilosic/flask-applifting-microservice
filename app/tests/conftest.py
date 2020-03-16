import os
import tempfile

import pytest
 
from flask import current_app
from app import create_app, db


@pytest.fixture(scope='module')
def client():
    app = create_app()
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    
 
    # Establish an application context before running the tests.
    with app.test_client() as client:
        yield client

    
 
 

    

