import requests
from .exceptions import OpenRouterError, OpenRouterAuthenticationError, OpenRouterRequestError

class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5000",  # Your site URL
            "X-Title": "SS Content Writer",  # Your site name
            "Content-Type": "application/json"
        }
        
    def chat_completion(self, messages, model="anthropic/claude-3.5-sonnet", max_tokens=1000):
        """
        Get a chat completion from OpenRouter
        
        Args:
            messages (list): List of message dicts with 'role' and 'content'
            model (str): Model to use (default: anthropic/claude-3.5-sonnet)
            max_tokens (int): Maximum tokens in response
            
        Returns:
            dict: Response from OpenRouter
        """
        try:
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self._get_headers(),
                json=payload
            )
            
            if response.status_code == 401:
                raise OpenRouterAuthenticationError("Invalid API key")
            elif response.status_code == 400:
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                raise OpenRouterRequestError(f"Bad request: {error_detail}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise OpenRouterRequestError(f"Request failed: {str(e)}") 