import requests
import redis
from functools import wraps
from typing import Callable

# Create a Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def track_access_count(url: str) -> None:
    count_key = f"count:{url}"
    redis_client.incr(count_key)

def cache_with_expiry(url: str, content: str) -> None:
    cache_key = f"cache:{url}"
    redis_client.setex(cache_key, 10, content)

def get_page(url: str) -> str:
    # Check if the content is cached
    cache_key = f"cache:{url}"
    cached_content = redis_client.get(cache_key)

    if cached_content:
        track_access_count(url)
        return cached_content.decode('utf-8')

    # Fetch content using requests
    response = requests.get(url)
    content = response.text

    # Cache the content with an expiry time of 10 seconds
    cache_with_expiry(url, content)
    track_access_count(url)

    return content

# Decorator to add caching and tracking to functions
def web_cache(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        # Check if the content is cached
        cache_key = f"cache:{url}"
        cached_content = redis_client.get(cache_key)

        if cached_content:
            track_access_count(url)
            return cached_content.decode('utf-8')

        # Execute the original function
        content = func(url)

        # Cache the content with an expiry time of 10 seconds
        cache_with_expiry(url, content)
        track_access_count(url)

        return content

    return wrapper

# Usage of the decorator
@web_cache
def get_page_with_cache(url: str) -> str:
    # Fetch content using requests
    response = requests.get(url)
    content = response.text
    return content

# Example usage
if __name__ == "__main__":
    # Example usage of the get_page function
    url_to_fetch = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.example.com"
    result = get_page(url_to_fetch)
    print(f"Content fetched from {url_to_fetch}:\n{result}")

    # Example usage of the decorated get_page_with_cache function
    url_to_fetch_cached = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.example.com"
    result_cached = get_page_with_cache(url_to_fetch_cached)
    print(f"\nContent fetched from {url_to_fetch_cached} using caching:\n{result_cached}")

    # Example tracking the access count
    access_count_key = f"count:{url_to_fetch}"
    count = redis_client.get(access_count_key)
    print(f"\nAccess count for {url_to_fetch}: {int(count)}")
