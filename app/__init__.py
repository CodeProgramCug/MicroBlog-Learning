from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__, instance_relative_config = True)
app.config.from_pyfile('config.py')
track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

# Mongodb
app.config['MONGODB_SETTINGS'] = {
    'db': 'myweb',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

# For login_manager init
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Please login"



from app import models
from app import views