from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
#from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
#csrf = CSRFProtect(app)
#app.secret_key = 'oracle'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/lightsouttool'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from my_app.product.views import app



db.create_all()


