#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable

def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - checks whether a URL's data is cached
            - tracks how many times get_page is called
        """
        # Create a Redis client
        client = redis.Redis()

        # Increment the access count for the URL
        client.incr(f'count:{url}')

        # Check if cached data exists for the URL
        cached_page = client.get(f'{url}')
        if cached_page:
            # Return cached data if available
            return cached_page.decode('utf-8')

        # Call the original function to fetch data
        response = fn(url)

        # Cache the response with a 10-second expiration
        client.setex(f'{url}', 10, response)

        # Return the fetched data
        return response

    return wrapper

@track_get_page
def get_page(url: str) -> str:
    """ Makes an HTTP request to a given endpoint
    """
    # Make an HTTP request using the requests module
    response = requests.get(url)

    # Return the text content of the response
    return response.text

# Example usage
if __name__ == "__main__":
    # Example of calling the get_page function with caching
    url_to_fetch = "https://www.example.com"
    result = get_page(url_to_fetch)
    
    # Print the result
    print(f"Content fetched from {url_to_fetch}:\n{result}")
