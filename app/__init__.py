from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])

    with app.app_context():

        # Create tables for our models
        db.create_all()

        return app