# Push and pop from a list
redis_client.lpush('my_list', 'item1')
redis_client.rpush('my_list', 'item2')

# Get all elements in the list
my_list = redis_client.lrange('my_list', 0, -1)
print(my_list)

