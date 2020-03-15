from datetime import datetime
import requests
import os

from flask_restful import Resource, reqparse, abort
from flask import jsonify

from app import db
from app.models import Product, Offer
from app.functions import register_product, refresh_offer_prices

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Product name is required', required=True)
parser.add_argument('description', type=str, help='Product description is required', required=True)

class ProductListAPI(Resource):
    "Api for getting a list"
    def get(self):
        products = Product.query.all()
        return jsonify([product.serialize for product in products])

    def post(self):
        args = parser.parse_args()
        existing_product = Product.query.filter_by(name=args["name"]).first()

        if existing_product:
            abort(409)

        product = Product(
            name=args['name'], 
            description=args['description']
            )
        db.session.add(product)
        db.session.commit()

        register_product(product)
        return jsonify(product.serialize)


class ProductAPI(Resource):
    "Api endpoints for CRUD of a product"
    def get(self, id):
        product = Product.query.filter_by(id=id).first_or_404()
        return jsonify(product.serialize)
    
    def put(self,id):
        product = Product.query.filter_by(id=id).first_or_404()
        args = parser.parse_args()
        product.name= args['name']
        product.description = args['description']
        product.updated = datetime.now()
        db.session.commit()
        return jsonify(product.serialize)
    
    def delete(self, id):
        product = Product.query.filter_by(id=id).first_or_404()
        product.deleted = datetime.now()
        db.session.commit()
        return jsonify(product.serialize)


class JobsAPI(Resource):
    def post(self):
        do_async_task.delay()