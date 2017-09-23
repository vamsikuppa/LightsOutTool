# Configurations
class BaseConfig(object):
    """Base config class"""
    SECRET_KEY = 'oracle'
    DEBUG = True
    TESTING = False
    # NEW_CONFIG_VARIABLE = 'my value'


class ProductionConfig(BaseConfig):
    """Production specific config"""
    DEBUG = False
    # SECRET_KEY = open('/path/to/secret/file').read()
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/lightsouttool'


class StagingConfig(BaseConfig):
    """Staging specific config"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/lightsouttool'

class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    TESTING = True
    # SECRET_KEY = 'Another random secret key'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/lightsouttool'
