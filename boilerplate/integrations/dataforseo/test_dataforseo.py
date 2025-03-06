#!/usr/bin/env python
"""
Test script for DataForSEO integration.
Run this script from the terminal to verify the DataForSEO integration works correctly.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the project root to the path so we can import boilerplate
# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up 3 directories to reach the project root
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
# Add to Python path
sys.path.insert(0, project_root)

# Now we can import from boilerplate
from boilerplate.integrations.dataforseo.client import DataForSEOClient
from boilerplate.integrations.dataforseo.services import SEODataService
from boilerplate.integrations.dataforseo.exceptions import DataForSEOError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dataforseo_test")

def test_client():
    """Test the DataForSEO client connection"""
    logger.info("Testing DataForSEO client...")
    
    # Try API key first
    api_key = os.environ.get('DATAFORSEO_API_KEY')
    
    # If no API key, try username/password
    if not api_key:
        username = os.environ.get('DATAFORSEO_USERNAME')
        password = os.environ.get('DATAFORSEO_PASSWORD')
        
        if username and password:
            api_key = f"{username}:{password}"
    
    if not api_key:
        logger.error("Either DATAFORSEO_API_KEY or both DATAFORSEO_USERNAME and DATAFORSEO_PASSWORD must be set")
        return False
        
    try:
        client = DataForSEOClient(api_key=api_key)
        connection_status = client.test_connection()
        
        if connection_status:
            logger.info("✅ Connection to DataForSEO API successful!")
            return True
        else:
            logger.error("❌ Connection test failed but did not raise an exception")
            return False
            
    except DataForSEOError as e:
        logger.error(f"❌ DataForSEO connection error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return False

def test_service():
    """Test the DataForSEO service functionality"""
    logger.info("Testing SEO data service...")
    
    try:
        service = SEODataService()
        
        # Test keyword analysis
        test_keyword = "python programming"
        logger.info(f"Analyzing keyword: '{test_keyword}'")
        
        result = service.analyze_keyword(test_keyword)
        
        if result:
            logger.info(f"✅ Successfully analyzed keyword. Task ID: {result.get('task_id')}")
            return True
        else:
            logger.error("❌ Keyword analysis returned no result")
            return False
            
    except ValueError as e:
        logger.error(f"❌ Service error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return False

def run_tests():
    """Run all tests and return overall status"""
    # Find the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    
    # Possible .env file locations, in order of preference
    possible_env_paths = [
        os.path.join(project_root, 'project', '.env'),            # Production setup
        os.path.join(project_root, 'example-project', '.env'),    # Example project setup
        os.path.join(project_root, '.env')                        # Root .env
    ]
    
    # Try each path until we find one that exists
    env_loaded = False
    for env_path in possible_env_paths:
        if os.path.isfile(env_path):
            load_dotenv(env_path)
            logger.info(f"Loaded environment from: {env_path}")
            env_loaded = True
            break
    
    if not env_loaded:
        logger.warning("No .env file found in standard locations. Using existing environment variables.")
    
    logger.info(f"DATAFORSEO_USERNAME: {'*****' if os.environ.get('DATAFORSEO_USERNAME') else 'Not Found'}")
    logger.info(f"DATAFORSEO_PASSWORD: {'*****' if os.environ.get('DATAFORSEO_PASSWORD') else 'Not Found'}")
    
    logger.info("Starting DataForSEO integration tests...")
    
    client_success = test_client()
    
    # Only test service if client test succeeded
    if client_success:
        service_success = test_service()
    else:
        logger.warning("Skipping service test due to client connection failure")
        service_success = False
    
    # Overall success
    if client_success and service_success:
        logger.info("🎉 All DataForSEO tests passed successfully!")
        return 0
    else:
        logger.error("❌ Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    # When run directly from terminal
    sys.exit(run_tests()) 