from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate

from celery import Celery
from app import celeryconfig


# global db instance
db = SQLAlchemy()

# global session instance
sess = Session()

# global celery instance 
celery = Celery(__name__, broker=celeryconfig.CELERY_BROKER_URL,
include=['app.functions'])

# global migrate instance
migrate = Migrate()

from app.models import Product, Offer


def create_app():
    """Construct the core application."""
    # configure Flask app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevelopmentConfig')
    
    # configure celery
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)

    # celery.conf.update(app.config)

    # initialize db
    db.init_app(app)
    app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])

    # migrate model changes
    migrate.init_app(app, db)


    # initialize session
    sess.init_app(app)

    with app.app_context():

        # Create tables for our models
        db.create_all()
        return app