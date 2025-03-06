from boilerplate.integrations.dataforseo.client import DataForSEOClient
from boilerplate.integrations.dataforseo.exceptions import DataForSEOError
import os
import logging
import time

logger = logging.getLogger(__name__)

class SEODataService:
    def __init__(self, api_key=None):
        """Initialize SEO data service
        
        Args:
            api_key (str, optional): DataForSEO API key (username:password), 
                                    defaults to env var
        """
        # Try to get API key from environment if not provided
        api_key = api_key or os.environ.get('DATAFORSEO_API_KEY')
        
        # If no API key, try username/password from environment
        if not api_key:
            username = os.environ.get('DATAFORSEO_USERNAME')
            password = os.environ.get('DATAFORSEO_PASSWORD')
            if username and password:
                api_key = f"{username}:{password}"
                
        self.client = DataForSEOClient(api_key=api_key)
    
    def analyze_keyword(self, keyword, location="United Kingdom"):
        """Analyze a keyword and return SERP data
        
        Args:
            keyword (str): The keyword to analyze
            location (str, optional): Location name, defaults to 'United Kingdom'
            
        Returns:
            dict: Processed SERP data
        """
        try:
            # Use the live SERP search directly
            # UK location code is 2826
            location_code = 2826 if location == "United Kingdom" else 2840  # Default to US (2840)
            
            response = self.client.search_serp_live(keyword, location_code=location_code)
            
            # Process the successful response
            if not response.get("tasks"):
                logger.error(f"No tasks found in response for keyword: {keyword}")
                return None
                
            # Extract relevant data from response
            task = response["tasks"][0]
            result = {
                "keyword": keyword,
                "location": location,
                "status": "completed",
                "search_engine": "google",
                "results_count": task.get("result_count", 0),
                "total_count": task.get("result", [{}])[0].get("se_results_count", 0) if task.get("result") else 0
            }
            
            # Include some items if available
            if task.get("result") and len(task["result"]) > 0 and "items" in task["result"][0]:
                result["top_items"] = task["result"][0]["items"][:5] if len(task["result"][0]["items"]) >= 5 else task["result"][0]["items"]
            
            return result
            
        except DataForSEOError as e:
            logger.error(f"DataForSEO error: {str(e)}")
            raise ValueError(f"Keyword analysis failed: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error in keyword analysis")
            raise ValueError(f"Keyword analysis failed: {str(e)}") 