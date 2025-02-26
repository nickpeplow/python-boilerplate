class WordPressError(Exception):
    """Base exception for WordPress integration"""
    pass

class WordPressConnectionError(WordPressError):
    """Raised when connection to WordPress site fails"""
    pass

class WordPressAuthenticationError(WordPressError):
    """Raised when authentication fails"""
    pass 