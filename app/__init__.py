import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from werkzeug import secure_filename
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

#Login_serializer used to encryt and decrypt the cookie token for the remember
#me option of flask-login
#login_serializer = URLSafeTimedSerializer(app.secret_key)
 
#Flask-Login Login Manager
login_manager = LoginManager()
#Tell the login manager where to redirect users to display the login page
login_manager.login_view = "/login/"
#Setup the login manager. 
login_manager.setup_app(app)    


from app import views, models

@app.template_filter()
def datetimefilter(value, format='%B %Y'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter






