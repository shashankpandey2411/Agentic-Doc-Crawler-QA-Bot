import logging
import time
from functools import wraps
import requests

def handle_request_error(url, error):
    """Handle errors during web requests."""
    if isinstance(error, requests.exceptions.ConnectionError):
        logging.error(f"Connection error when accessing {url}: {error}")
    elif isinstance(error, requests.exceptions.Timeout):
        logging.error(f"Timeout when accessing {url}: {error}")
    elif isinstance(error, requests.exceptions.HTTPError):
        status_code = error.response.status_code if hasattr(error, 'response') else 'unknown'
        logging.error(f"HTTP error {status_code} when accessing {url}: {error}")
    else:
        logging.error(f"Error when accessing {url}: {error}")

def retry_on_error(max_retries=3, backoff_factor=2):
    """Decorator for retrying functions on failure with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait_time = backoff_factor ** retries
                    retries += 1
                    
                    if retries <= max_retries:
                        logging.warning(f"Retrying in {wait_time} seconds after error: {e}")
                        time.sleep(wait_time)
                    else:
                        logging.error(f"Failed after {max_retries} retries: {e}")
                        raise
        return wrapper
    return decorator 