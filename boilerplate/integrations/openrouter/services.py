from .client import OpenRouterClient
from .exceptions import OpenRouterError
import os
import logging

logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self):
        self.client = OpenRouterClient(
            api_key=os.environ.get('OPENROUTER_API_KEY')
        )
    
    def generate_content(self, prompt, context=None):
        """
        Generate content using OpenRouter
        
        Args:
            prompt (str): The main prompt
            context (dict, optional): Additional context
            
        Returns:
            str: Generated content
        """
        try:
            messages = []
            
            # Add context if provided
            if context:
                messages.append({
                    "role": "system",
                    "content": str(context)
                })
            
            # Add user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            response = self.client.chat_completion(messages)
            
            # Extract the response text
            if response.get('choices') and len(response['choices']) > 0:
                return response['choices'][0]['message']['content']
            else:
                return None
                
        except OpenRouterError as e:
            logger.error(f"OpenRouter error: {str(e)}")
            raise ValueError(f"Content generation failed: {str(e)}") 