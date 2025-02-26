import requests
from urllib.parse import urljoin
from .exceptions import WordPressConnectionError, WordPressAuthenticationError

class WordPressClient:
    def __init__(self, url, username, app_password):
        self.url = url.rstrip('/')  # Remove trailing slash
        self.username = username
        self.app_password = app_password
        
    def test_connection(self):
        """Test connection to WordPress site"""
        try:
            # First, check if the site is reachable
            response = requests.get(
                self.url,
                timeout=10,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Then check if REST API is available
            rest_url = urljoin(self.url, 'wp-json/')
            response = requests.get(
                rest_url,
                timeout=10
            )
            if response.status_code == 404:
                raise WordPressConnectionError("WordPress REST API not found. Please ensure the site has REST API enabled.")
                
            # Finally test authentication
            auth_url = urljoin(self.url, 'wp-json/wp/v2/users/me')
            response = requests.get(
                auth_url,
                auth=(self.username, self.app_password),
                timeout=10
            )
            
            if response.status_code == 401:
                raise WordPressAuthenticationError("Invalid application password")
            elif response.status_code != 200:
                raise WordPressConnectionError(f"API request failed with status {response.status_code}")
                
            return True
            
        except requests.exceptions.ConnectionError as e:
            raise WordPressConnectionError("Could not connect to WordPress site. Please check the URL and ensure the site is accessible.")
        except requests.exceptions.Timeout:
            raise WordPressConnectionError("Connection timed out. Please check your internet connection and try again.")
        except requests.exceptions.RequestException as e:
            raise WordPressConnectionError(f"Connection failed: {str(e)}") 