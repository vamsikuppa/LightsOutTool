from my_app import app
from my_app import manager
from flask_wtf.csrf import CSRFProtect

#manager.run()

csrf = CSRFProtect(app)
app.secret_key = 'oracle'
app.run(debug=True)
