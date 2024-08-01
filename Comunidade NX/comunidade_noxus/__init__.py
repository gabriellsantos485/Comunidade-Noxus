from flask import Flask                                                                                
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b5d39209fbf531b21a5cbd041d6d2947'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comunidade.db"
bcrypt=Bcrypt()
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

database=SQLAlchemy(app)

from comunidade_noxus import routes
