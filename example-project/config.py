import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from project's .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path, override=True)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'project/.env'))

# Project specific configuration
APP_NAME = os.environ.get('APP_NAME', 'Example App')
APP_DESCRIPTION = os.environ.get('APP_DESCRIPTION', 'A boilerplate Flask application')

# Database URL for this project
DATABASE_URL = (
    f"mysql+pymysql://"
    f"{os.environ.get('DB_USERNAME')}:"
    f"{os.environ.get('DB_PASSWORD')}@"
    f"{os.environ.get('DB_HOST')}:"
    f"{os.environ.get('DB_PORT')}/"
    f"{os.environ.get('DB_NAME')}"
)

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY')

# Flask settings
FLASK_APP = os.environ.get('FLASK_APP', 'app.py')
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'

# WordPress API settings
WP_API_TIMEOUT = int(os.environ.get('WP_API_TIMEOUT', 30))
WP_API_RETRIES = int(os.environ.get('WP_API_RETRIES', 3)) 