from my_app import app
from my_app import manager
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

#manager.run()

csrf = CSRFProtect(app)
#app.secret_key = 'oracle'
#app.run(debug=True)
app.config.from_object('config.ProductionConfig')
app.run()
