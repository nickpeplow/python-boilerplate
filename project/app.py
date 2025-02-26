from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from boilerplate.config import Config
from boilerplate.database import init_db, db
from boilerplate.auth.models import User
from boilerplate.auth import auth_bp
from boilerplate.core import core_bp
from project.project import APP_NAME, APP_DESCRIPTION, NAVIGATION
from boilerplate.app import create_base_app
import os
import logging
from .cli import generate_examples_command
from project.example import example_bp

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_app():
    # Get base app
    app = create_base_app()
    
    # Add boilerplate templates directory
    app.jinja_loader.searchpath.append(os.path.join(app.root_path, '../boilerplate/core/templates'))
    
    # Register project blueprints
    app.register_blueprint(example_bp)

    # Project configuration
    app.config['APP_NAME'] = APP_NAME
    app.config['APP_DESCRIPTION'] = APP_DESCRIPTION
    app.config['NAVIGATION'] = NAVIGATION

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Add root route
    @app.route('/')
    def index():
        return redirect(url_for('example.list'))

    app.cli.add_command(generate_examples_command)

    return app

app = create_app()

if __name__ == '__main__':
    app.run() 