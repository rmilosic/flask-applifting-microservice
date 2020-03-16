import os
import redis

class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_TYPE='filesystem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
