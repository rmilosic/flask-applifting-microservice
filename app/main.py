from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from . import create_app
from app.resources import IndexResource, ProductResource

app = create_app()

api = Api(app)

api.add_resource(ProductResource, '/product', '/product/new')
api.add_resource(IndexResource, '/')


if __name__ == '__main__':
    app.run(debug=True)