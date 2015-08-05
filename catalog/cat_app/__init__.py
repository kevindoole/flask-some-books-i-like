import os
import json
from flask import Flask
from flask import session as login_session
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'storage/catalog.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = 'blurfschkie'
db = SQLAlchemy(app)

from cat_app import models
from .views.auth import auth
from .views.admin import admin
from .views.frontend import frontend

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(frontend)