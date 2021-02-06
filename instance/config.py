import os


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "epam"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False