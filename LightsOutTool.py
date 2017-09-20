from my_app import app
from my_app import manager
from flask_wtf.csrf import CSRFProtect

#manager.run()

csrf = CSRFProtect(app)
app.secret_key = 'oracle'
app.run(debug=True)

#Configurations
# class BaseConfig(object):
#     """Base config class"""
#     SECRET_KEY = 'oracle'
#     DEBUG = True
#     TESTING = False
#     NEW_CONFIG_VARIABLE = 'my value'
#
#
# class ProductionConfig(BaseConfig):
#     """Production specific config"""
#     DEBUG = False
#     # SECRET_KEY = open('/path/to/secret/file').read()
#
#
# class StagingConfig(BaseConfig):
#     """Staging specific config"""
#     DEBUG = True
#
#
# class DevelopmentConfig(BaseConfig):
#     """Development environment specific config"""
#     DEBUG = True
#     TESTING = True
#     # SECRET_KEY = 'Another random secret key'

