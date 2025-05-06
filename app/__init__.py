import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate  = Migrate()
login_manager = LoginManager()
bcrypt  = Bcrypt()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Load configuration
    if config_class is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_object(config_class)
    
    #set default config
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 
                         f'sqlite:///{os.path.join(app.instance_path, "book_app.db")}')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.congig.setdefault('SECRET_KEY', 'dev-key-please-change-in-production')

    # Intialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
