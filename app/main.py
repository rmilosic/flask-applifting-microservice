from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app

# create Flask app with app factory


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')