from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from app.instance import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app():
    __app__ = Flask(__name__)
    __app__.config.from_object(config.Dev)

    import app.models

    db.init_app(__app__)
    migrate.init_app(__app__, db)
    login_manager.init_app(__app__)
    mail.init_app(__app__)

    return __app__

