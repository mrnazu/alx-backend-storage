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

