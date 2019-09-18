import os
import redis
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_wtf.csrf import CSRFProtect


base_dir = os.path.dirname(os.path.abspath(__file__))
rds = redis.StrictRedis.from_url(os.environ.get('REDIS_URL'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('FLASK_DEBUG', False) in ('1', 'True')
app.config['SESSION_COOKIE_NAME'] = 'bookhub-session'
app.config['REMEMBER_COOKIE_NAME'] = 'bookhub-remember-me'
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_KEY_PREFIX'] = 'bookhub:session:'
app.config['SESSION_REDIS'] = rds

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
Session(app)
csrf = CSRFProtect(app)
