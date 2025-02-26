class OpenRouterError(Exception):
    """Base exception for OpenRouter integration"""
    pass

class OpenRouterAuthenticationError(OpenRouterError):
    """Raised when API key is invalid"""
    pass

class OpenRouterRequestError(OpenRouterError):
    """Raised when request to OpenRouter fails"""
    pass 