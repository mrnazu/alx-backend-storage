# redis-py - Python Client for Redis

`redis-py` is a Python client library for interacting with Redis, which is an in-memory data structure store often used as a cache, message broker, or general-purpose key-value store. The `redis-py` library allows Python applications to communicate with Redis servers.

Here's a basic overview and some common operations using `redis-py`:

### Installation:

You can install `redis-py` using pip:

```bash
pip install redis
```

### Basic Usage:

```python
import redis

# Connect to a Redis server (default is localhost on port 6379)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Set a key-value pair
redis_client.set('sayHello', 'Hey, this is nazu!')

# Get the value by key
value = redis_client.get('sayHello')
print(value.decode('utf-8'))  # Decode bytes to string

# Delete a key
redis_client.delete('sayHello')
```

### Working with Data Types:

#### Strings:

```python
# Set and get a string
redis_client.set('my_string', 'Hello, Redis!')
value = redis_client.get('my_string')
print(value.decode('utf-8'))

# Append to a string
redis_client.append('my_string', ' How are you?')
value = redis_client.get('my_string')
print(value.decode('utf-8'))
```

#### Lists:

```python
# Push and pop from a list
redis_client.lpush('my_list', 'item1')
redis_client.rpush('my_list', 'item2')

# Get all elements in the list
my_list = redis_client.lrange('my_list', 0, -1)
print(my_list)
```

#### Sets:

```python
# Add and remove elements from a set
redis_client.sadd('my_set', 'element1')
redis_client.sadd('my_set', 'element2')

# Get all elements in the set
my_set = redis_client.smembers('my_set')
print(my_set)
```

#### Hashes:

```python
# Set and get values in a hash
redis_client.hset('my_hash', 'field1', 'value1')
redis_client.hset('my_hash', 'field2', 'value2')

# Get all field-value pairs in the hash
my_hash = redis_client.hgetall('my_hash')
print(my_hash)
```

These are just some basic examples to get you started with `redis-py`. The library provides many more features and options for working with Redis. Make sure to check the official documentation for more details: [redis-py documentation](https://redis-py.readthedocs.io/).
