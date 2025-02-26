"""
Main application entry point.
"""
from project.app import app

if __name__ == '__main__':
    app.run(debug=True) 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(example_bp, url_prefix='/example')