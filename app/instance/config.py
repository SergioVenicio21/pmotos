class BaseConfig():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'sergiovenicio2015@gmail.com'
    MAIL_PASSWORD = 'emsssxnydvlhndqb'
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = False


class Dev(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://pamotos_user:pamotos_pwd@localhost/pamotos'


class Prod():
    SQLALCHEMY_DATABASE_URI = 'postgresql://pamotos_user:pamotos_pwd@localhost/pamotos'
