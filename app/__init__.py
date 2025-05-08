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

    #configure_login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    #register blueprints
    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app    
