from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
import os
from project.config import DATABASE_URL

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def init_database():
    try:
        # Get database name from environment
        db_name = os.environ.get('DB_NAME')
        
        # Create base URL without database name
        base_url = DATABASE_URL.rsplit('/', 1)[0]

        # Create engine without database name
        engine = create_engine(base_url)
        with engine.connect() as conn:
            # Create database using exact name from environment
            create_db_sql = f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            conn.execute(text(create_db_sql))
            conn.execute(text(f"USE `{db_name}`"))
            logging.info(f"Database '{db_name}' created successfully")

    except Exception as e:
        logging.error(f"Database initialization error: {str(e)}")
        raise

def init_db(app):
    """Initialize the database with the app context"""
    try:
        # Create database if it doesn't exist
        init_database()

        # Initialize Flask-SQLAlchemy
        db.init_app(app)
        
        with app.app_context():
            # Create/update tables
            db.create_all()
            logging.info("Database tables created/updated successfully")
        
    except Exception as e:
        logging.error(f"Database initialization error: {str(e)}")
        raise

def get_db():
    """Helper function to get db instance"""
    return db

def close_db(e=None):
    """Helper function to close db connection"""
    db.session.remove() 