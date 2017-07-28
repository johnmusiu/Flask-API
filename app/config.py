''' my config file '''
import os

class BaseConfig(object):
    ''' defines the base config, used in deployed api '''
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SECRET_KEY = os.getenv('SECRET_KEY')
    #FLASK_APP='run.py'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:kotiPC12#@localhost:5432/flask_api_db"
    SECRET_KEY = "my long secure little secret"
    #APP_SETTING = "DevelopmentConfig"
    

class DevelopmentConfig(BaseConfig):
    """ Development env imports BaseConfig and sets DEBUG and TESTING to True """
    DEBUG = True
    TESTING = True

class TestingConfig(BaseConfig):
    ''' passs test db for testing purposes'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:kotiPC12#@localhost:5432/test_db"

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'base': BaseConfig,
}
