import os
import redis

class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_TYPE='filesystem'
    

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}"

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}"
    DEBUG = True

class TestingConfig(Config):
    TESTING = True