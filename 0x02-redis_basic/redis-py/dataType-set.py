# Add and remove elements from a set
redis_client.sadd('my_set', 'element1')
redis_client.sadd('my_set', 'element2')

# Get all elements in the set
my_set = redis_client.smembers('my_set')
print(my_set)

