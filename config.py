import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # put own data base 
    DEBUG = True


class TextingConfig:
    pass

class ProductionConfig:
    pass