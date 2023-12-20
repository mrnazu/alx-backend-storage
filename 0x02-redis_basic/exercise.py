import uuid
import redis
from typing import Union

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        # Initialize the Redis client and flush the database
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        # Generate a random key using uuid
        key = str(uuid.uuid4())

        # Store the data in Redis with the generated key
        if isinstance(data, (int, float)):
            # Convert int or float to string before storing
            data = str(data)

        self._redis.set(key, data)

        # Return the generated key
        return key

# Example usage:
cache_instance = Cache()
key = cache_instance.store("Hello, Redis!")
print(f"Data stored with key: {key}")

