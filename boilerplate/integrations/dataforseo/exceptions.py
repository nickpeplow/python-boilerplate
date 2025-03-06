class DataForSEOError(Exception):
    """Base exception for DataForSEO integration"""
    pass

class DataForSEOAuthenticationError(DataForSEOError):
    """Raised when API authentication fails"""
    pass

class DataForSEORequestError(DataForSEOError):
    """Raised when request to DataForSEO fails"""
    pass

class DataForSEOQuotaExceededError(DataForSEOError):
    """Raised when the API quota is exceeded"""
    pass 