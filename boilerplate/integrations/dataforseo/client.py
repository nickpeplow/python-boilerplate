import requests
import base64
import json
from boilerplate.integrations.dataforseo.exceptions import (
    DataForSEOError, 
    DataForSEOAuthenticationError, 
    DataForSEORequestError,
    DataForSEOQuotaExceededError
)
import logging

logger = logging.getLogger(__name__)

class DataForSEOClient:
    """Client for interacting with the DataForSEO API"""
    
    BASE_URL = "https://api.dataforseo.com/v3"
    
    def __init__(self, api_key=None, username=None, password=None):
        """Initialize client with either API key or username/password
        
        Args:
            api_key (str, optional): API key in format "username:password"
            username (str, optional): DataForSEO username
            password (str, optional): DataForSEO password
        """
        # Support both API key format or separate username/password
        if api_key and ':' in api_key:
            self.username, self.password = api_key.split(':', 1)
        else:
            self.username = username
            self.password = password
            
        if not self.username or not self.password:
            raise DataForSEOAuthenticationError(
                "Either api_key in format 'username:password' or both username and password must be provided"
            )
        
    def _get_auth_header(self):
        """Generate the basic auth header for DataForSEO API"""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        
        # Log the encoded credentials for debugging (partially obscured)
        encoded_prefix = encoded_credentials[:10] if len(encoded_credentials) > 10 else encoded_credentials
        logger.debug(f"Encoded auth credentials prefix: {encoded_prefix}...")
        
        return {"Authorization": f"Basic {encoded_credentials}"}
    
    def _make_request(self, method, endpoint, data=None):
        """Make a request to the DataForSEO API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint (without base URL)
            data (dict, optional): Data to send with the request
            
        Returns:
            dict: Response from DataForSEO
        """
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            **self._get_auth_header(),
            "Content-Type": "application/json"
        }
        
        try:
            logger.debug(f"Making {method} request to {url}")
            if data:
                logger.debug(f"Request data: {json.dumps(data)}")
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=60)
            elif method.upper() == "POST":
                response = requests.post(
                    url, 
                    headers=headers, 
                    data=json.dumps(data) if data else None,
                    timeout=60
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Log the raw response for debugging
            logger.debug(f"Response status code: {response.status_code}")
            
            # Handle HTTP errors
            if response.status_code == 401:
                raise DataForSEOAuthenticationError("Invalid API credentials")
            elif response.status_code == 429:
                raise DataForSEOQuotaExceededError("API rate limit exceeded")
            
            # Try to parse the response as JSON
            try:
                response_data = response.json()
                logger.debug(f"Response data: {json.dumps(response_data)}")
            except ValueError:
                # If not JSON, raise an error with the response text
                logger.error(f"Invalid JSON response: {response.text}")
                raise DataForSEORequestError(f"Invalid JSON response: {response.text[:100]}...")
            
            # Check for error responses - DataForSEO uses status_code, not status
            if response_data.get("status_code") != 20000:  # 20000 is success
                error_message = response_data.get("status_message", "Unknown error")
                        
                # Try to extract errors from tasks array
                if "tasks" in response_data and response_data["tasks"]:
                    for task in response_data["tasks"]:
                        if task.get("status_code") != 20000:
                            error_message = task.get("status_message", error_message)
                            break
                            
                raise DataForSEORequestError(f"API request failed: {error_message}")
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            raise DataForSEORequestError(f"Request failed: {str(e)}")
    
    def test_connection(self):
        """Test connection to DataForSEO API
        
        Returns:
            bool: True if connection successful
        """
        try:
            # Test with a simple endpoint
            url = f"{self.BASE_URL}/keywords_data/google/locations"
            headers = {
                **self._get_auth_header(),
                "Content-Type": "application/json"
            }
            
            logger.info(f"Making direct request to: {url}")
            response = requests.get(url, headers=headers, timeout=60)
            
            # Log the full response for debugging
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                resp_json = response.json()
                # Check for DataForSEO success code
                if resp_json.get('status_code') == 20000:
                    logger.info("Successfully connected to DataForSEO API")
                    return True
            except:
                logger.error("Failed to parse response as JSON")
            
            # If initial request failed, try with a simple POST request
            url = f"{self.BASE_URL}/serp/google/organic/live/advanced"
            data = [{
                "keyword": "test",
                "location_code": 2826,  # UK
                "language_code": "en"
            }]
            
            logger.info("Trying SERP request...")
            response = requests.post(
                url, 
                headers=headers, 
                data=json.dumps(data),
                timeout=60
            )
            
            try:
                resp_json = response.json()
                # Check for DataForSEO success code
                if resp_json.get('status_code') == 20000:
                    logger.info("Successfully connected to DataForSEO API with SERP request")
                    return True
            except:
                logger.error("Failed to parse response as JSON")
            
            return False
            
        except Exception as e:
            import traceback
            logger.error(f"Connection test error: {str(e)}")
            logger.error(traceback.format_exc())
            raise DataForSEOError(f"Connection test failed: {str(e)}")
    
    def get_serp_results(self, keyword, location_code=2840, language_code="en", search_engine="google"):
        """Get SERP results for a keyword
        
        Args:
            keyword (str): Search term
            location_code (int): Location code (default: 2840 for US)
            language_code (str): Language code (default: 'en')
            search_engine (str): Search engine name (default: 'google')
            
        Returns:
            dict: SERP results data
        """
        data = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "device": "desktop"
        }]
        
        endpoint = f"serp/{search_engine}/organic/task_post"
        return self._make_request("POST", endpoint, data)
    
    def search_serp_live(self, keyword, location_code=2826, language_code="en", device="desktop", os="windows", depth=100):
        """
        Get live SERP results from Google
        
        Args:
            keyword (str): Search term
            location_code (int): Location code (default: 2826 for UK)
            language_code (str): Language code (default: 'en')
            device (str): Device type (default: 'desktop')
            os (str): Operating system (default: 'windows')
            depth (int): Results depth (default: 100)
            
        Returns:
            dict: SERP results response
        """
        data = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "device": device,
            "os": os,
            "depth": depth
        }]
        
        return self._make_request("POST", "serp/google/organic/live/advanced", data) 