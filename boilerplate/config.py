import os
from project.config import DATABASE_URL, SECRET_KEY

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Don't track migrations in the database during initialization
    SQLALCHEMY_MIGRATE_IGNORE = True
    
    # Security
    SECRET_KEY = SECRET_KEY
    
    # Navigation Menu
    NAVIGATION = [
        {
            'name': 'Sites',
            'url': 'sites.list',
            'active_route': 'sites'
        },
        {
            'name': 'Pages',
            'url': '#',
            'active_route': 'pages'
        },
        # ... other menu items ...
    ] 
    
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPENROUTER_SITE_URL = os.environ.get('OPENROUTER_SITE_URL', 'https://github.com/nickpeplow/ss-content-writer') 