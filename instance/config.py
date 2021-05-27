from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    TESTING = False
    SECRET_KEY = getenv('SECRET_KEY')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
