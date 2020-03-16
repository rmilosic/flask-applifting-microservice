from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from flask_restplus import Api

from celery import Celery

from app import celeryconfig


# api instance
api = Api()

# global db instance
db = SQLAlchemy()

# global session instance
sess = Session()

# global celery instance 
celery = Celery(__name__, )
celery.config_from_object(celeryconfig)

# global migrate instance
migrate = Migrate()



def create_app():
    """Construct the core application."""
    # configure Flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    app.config.from_envvar('APPLICATION_SETTINGS')
    
    initialize_extensions(app)
    register_blueprints(app)

    return app


def register_blueprints(app):

    from app.models import Product, Offer
    from app.resources import ProductAPI, ProductListAPI

    api.add_resource(ProductListAPI, '/products')
    api.add_resource(ProductAPI, '/products/<uuid:id>')
    

def initialize_extensions(app):

    # configure celery
    celery.conf.update(app.config)
    
    # initialize db
    db.init_app(app)

    # migrate model changes
    migrate.init_app(app, db)

    # initialize session
    sess.init_app(app)

    # init api
    api.init_app(app)

    
    
    # with app.app_context():

    #     # Create tables for our models
    #     db.create_all()

    #     return app