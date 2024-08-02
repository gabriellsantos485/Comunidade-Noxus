from flask import Flask, render_template, url_for, request, flash , redirect                                                                                    
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b5d39209fbf531b21a5cbd041d6d2947'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comunidade.db"
database = SQLAlchemy(app)
bcrypt=Bcrypt()
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from comunidade_noxus import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop.all()
        database.create_all()
        print("Base de dados criados")
else:
    print("Base de dados ja existente")


from comunidade_noxus import routes
