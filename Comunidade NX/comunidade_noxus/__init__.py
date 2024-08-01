from flask import Flask, render_template, url_for, request, flash , redirect                                                                                    
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b5d39209fbf531b21a5cbd041d6d2947'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ZGwjxcBIHBeMYBMfUyhEuWByBvbFfCEn@roundhouse.proxy.rlwy.net:49312/railway'
bcrypt=Bcrypt()
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

database=SQLAlchemy(app)

from comunidade_noxus import routes
