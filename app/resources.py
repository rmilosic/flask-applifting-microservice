from flask_restful import Resource, reqparse
from flask import jsonify

from app.models import Product, Offer
from app import db

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Product name')
parser.add_argument('description', type=str, help='Product description')

class ProductResource(Resource):
    def get(self):
        products = Product.query.all()
        return jsonify({"code": 200, "products": [product.serialize for product in products]})

    def post(self):
        args = parser.parse_args()
        product = Product(
            name=args['name'], 
            description=args['description']
            )
        db.session.add(product)
        db.session.commit()
        return jsonify(status_code=200, message="Successfully created a product", product_id=product.id)

    def delete(self):
        pass


class IndexResource(Resource):
    def get(self):
        return jsonify({"code": 200, "message": "Hello world"})