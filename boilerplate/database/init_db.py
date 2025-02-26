from boilerplate.database import db
from project.config import DATABASE_URL
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    try:
        # Parse DATABASE_URL to get connection details
        # mysql+pymysql://user:pass@host:port/dbname
        parts = DATABASE_URL.replace('mysql+pymysql://', '').split('/')
        db_name = parts[1]  # Use database name as-is from config
        credentials = parts[0].split('@')
        user_pass = credentials[0].split(':')
        host_port = credentials[1].split(':')

        config = {
            'user': user_pass[0],
            'password': user_pass[1],
            'host': host_port[0],
            'port': host_port[1]
        }

        # Create database if it doesn't exist
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        logger.info("Database tables created successfully")
        
        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

if __name__ == '__main__':
    init_database() 