# Set and get values in a hash
redis_client.hset('my_hash', 'field1', 'value1')
redis_client.hset('my_hash', 'field2', 'value2')

# Get all field-value pairs in the hash
my_hash = redis_client.hgetall('my_hash')
print(my_hash)

