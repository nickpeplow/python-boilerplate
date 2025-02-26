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
    