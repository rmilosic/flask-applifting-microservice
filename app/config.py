import os
import redis

class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_TYPE='filesystem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    SQLALCHEMY_DATABASE_URI=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
