import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

secret_key = 'sourcehaven'
expires_delta = datetime.timedelta(minutes=10)
host = 'localhost'
port = 5757


class Config:
    DEBUG = False
    TESTING = False
    HOST = host
    PORT = port
    CSRF_ENABLED = True
    SECRET_KEY = secret_key
    JWT_SECRET_KEY = secret_key
    JWT_ACCESS_TOKEN_EXPIRES = expires_delta
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SQLALCHEMY_DATABASE_URI = os.environ['MYPASS_DB_CONNECTION_URI']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
