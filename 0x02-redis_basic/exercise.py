import uuid
import redis
from typing import Union, Callable
from functools import wraps

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        if isinstance(data, (int, float)):
            data = str(data)
        self._redis.set(key, data)
        return key

    def replay(self, method: str):
        input_key = f"{method}:inputs"
        output_key = f"{method}:outputs"

        # Retrieve input and output history from Redis
        input_history = self._redis.lrange(input_key, 0, -1)
        output_history = self._redis.lrange(output_key, 0, -1)

        print(f"Replay for method: {method}\n")

        # Display input history
        print("Input History:")
        for i, entry in enumerate(input_history, 1):
            print(f"{i}. {entry.decode('utf-8')}")

        print("\nOutput History:")
        # Display output history
        for i, entry in enumerate(output_history, 1):
            print(f"{i}. {entry.decode('utf-8')}")

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is not None:
            return fn(data) if fn else data
        return None

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode('utf-8') if d else None)

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)

def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Append input parameters to the input list
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        result = method(self, *args, **kwargs)

        # Append the output to the output list
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper

# Example usage and test
cache = Cache()

# Calling store multiple times
for _ in range(3):
    cache.store("Hello, Redis!")

# Replay the history of calls for the store method
cache.replay("Cache.store")
