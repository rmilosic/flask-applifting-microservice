from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from . import create_app
from app.resources import ProductListAPI, ProductAPI, JobsAPI

# define custom API layer error exceptions
errors = {
    'Conflict': {
        'message': "A product with that username already exists.",
        'status': 409,
    },
}

# create Flask app with app factory
app = create_app()
# create API layer using app instance
api = Api(app, errors=errors)




api.add_resource(ProductListAPI, '/products')
api.add_resource(ProductAPI, '/products/<string:id>')
api.add_resource(JobsAPI, '/jobs/crawl-offers')



if __name__ == '__main__':
    app.run(debug=True)