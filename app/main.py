from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, api
from app.resources import ProductListAPI, ProductAPI

# create Flask app with app factory
app = create_app()


if __name__ == '__main__':
    app.run(debug=True)