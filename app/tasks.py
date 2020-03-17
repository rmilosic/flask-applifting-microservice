import requests

from flask import current_app

from app import celery
from app.models import Product, Offer



@celery.task()
def refresh_offer_prices() -> dict:
    """
    Celery task for retrieving offers and their prices for 
    individual products
    """
    with current_app.test_client() as client:
        response = client.post('/offers')

    return response.json
