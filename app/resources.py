from datetime import datetime
import requests
import os
import uuid

from flask import make_response, jsonify, current_app
from sqlalchemy.exc import IntegrityError
from flask_restplus import Resource, reqparse, abort, fields

from app import db, api
from app.models import Product, Offer
from app.functions import register_product, refresh_offer_prices


new_product_parser = reqparse.RequestParser()
new_product_parser.add_argument('name', type=str, help='Product name is required', required=True)
new_product_parser.add_argument('description', type=str, help='Product description is required', required=True)

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument('name', type=str, help='Product name')
update_product_parser.add_argument('description', type=str, help='Product description')


class ProductListAPI(Resource):
    "Api for getting a list of products"
    
    def get(self):
        """
        Get all products
        """
        products = Product.query.all()
        return make_response(jsonify([product.serialize for product in products]), 200)

    @api.expect(new_product_parser)
    @api.doc(params={
        "name": "Product name",
        "description": "Product description"
    })
    def post(self):
        """ 
        Create a product
        """
        args = new_product_parser.parse_args()

        product = Product(
            name=args['name'], 
            description=args['description']
            )
        try:
            db.session.add(product)
        except IntegrityError:
            abort(409, "Product with this name already exists")

        db.session.commit()

        # register the product with external service
        register_product(product)
        return make_response(jsonify(product.serialize), 201)


@api.doc(responses={
    404: "Product with provided ID not found"
})
class ProductAPI(Resource):
    "Api endpoints for CRUD of a product"
    
    def get(self, id):
        """
        Get a product by id
        """
        product = Product.query.filter_by(id=id).first_or_404()
        return make_response(jsonify(product.serialize), 200)
        
    @api.expect(update_product_parser)
    @api.doc(params={
        'id': 'Product id',
        'description': 'Product description',
        'name': 'Product name' 
    })
    def put(self, id):
        """
        Update a single product"
        """
        product = Product.query.filter_by(id=id).first_or_404()
        args = update_product_parser.parse_args()
        if args['name']:
            product.name = args['name']
        elif args["description"]:
            product.description = args['description']
        else:
            abort(409, 'No arguments provided')

        product.updated = datetime.now()
    
        try:
            db.session.commit()
        except IntegrityError:
            abort(409, "Product with this name already exists")

        return make_response(jsonify(product.serialize), 201)
    
    @api.doc(params={
        'id': 'Product id'
    })
    def delete(self, id):
        """
        Delete a single product
        """
        product = Product.query.filter_by(id=id).first_or_404()
        product.deleted = datetime.now()
        db.session.commit()
        return make_response(jsonify(product.serialize), 204)


class OfferListAPI(Resource):
    def get(self):
        """
        Get all tracked offers
        """
        offers = Offer.query.all()
        return make_response(jsonify([offer.serialize for offer in offers]), 200)

    def post(self):
        """
        Internal method for updating offers for stored products
        """
        response = refresh_offer_prices()
        current_app.logger.info(f"response: {response}")
        return make_response(jsonify(response), 200)


class ProductOfferListAPI(Resource):

    def get(self, product_id):
        """
        Gets a list of offers for a particular product
        """
        offers = Offer.query.filter_by(product_id=product_id).all()
        return make_response(jsonify([offer.serialize for offer in offers]), 200)


class OfferTrendAPI(Resource):

    def get(self, seller_id):
        """
        Gets an array of prices for a particular seller id
        """
        offer_prices = Offer.query.filter_by(seller_id=seller_id).with_entities(Offer.price).all()
        return make_response(jsonify(offer_prices), 200)

    