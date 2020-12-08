import os


class Config(object):

    DEBUG = bool(int(os.getenv('FLASK_DEBUG', '0')))
    TESTING = bool(int(os.getenv('FLASK_TESTING', '0')))
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'epam'