import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from flask_restplus import Api

from app import config, celeryconfig 
from celery import Celery

# api instance
api = Api()

# global db instance
db = SQLAlchemy()

# global session instance
sess = Session()

# global migrate instance
migrate = Migrate()

celery = Celery(__name__, config_source='app.celeryconfig')

def create_app():
    """Construct the core application."""
    # configure Flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.Config)
    app.config.from_envvar('APPLICATION_SETTINGS')
    
    
    initialize_extensions(app)
    register_blueprints(app)

    return app


def register_blueprints(app):

    
    from app.resources import ProductAPI, ProductListAPI, ProductOfferListAPI, OfferTrendAPI, OfferListAPI

    api.add_resource(ProductListAPI, '/products')
    api.add_resource(ProductAPI, '/products/<uuid:id>')
    api.add_resource(ProductOfferListAPI, '/products/<uuid:product_id>/offers')
    api.add_resource(OfferTrendAPI, '/offer/<int:seller_id>')
    api.add_resource(OfferListAPI, '/offers')

def initialize_extensions(app):
    
    from app.models import Product, Offer
    
    # initialize db
    db.init_app(app)

    # migrate model changes
    migrate.init_app(app, db)

    # initialize session
    sess.init_app(app)

    # init api
    api.init_app(app)

    init_celery(app, celery)
    
    with app.app_context():

        # Create tables for our models
        db.create_all()

    return app


def init_celery(app, celery):
    """Add flask app context to celery.Task"""
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
