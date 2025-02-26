"""
Base application factory for the boilerplate.

This provides core functionality that can be used by any project:
1. Basic Flask setup and configuration
2. Database initialization
3. Login manager setup
4. CSRF protection
5. Core blueprints (auth, core)
6. Basic logging configuration

Projects should import create_base_app() and extend it with
their own configuration and blueprints.
"""

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .config import Config
from .database import init_db, db
from .auth.models import User
from .auth import auth_bp
from .core import core_bp
import logging

def create_base_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Add CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Initialize database
    init_db(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register core blueprints
    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)

    return app 