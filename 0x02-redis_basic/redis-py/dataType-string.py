# Set and get a string
redis_client.set('my_string', 'Hello, Redis!')
value = redis_client.get('my_string')
print(value.decode('utf-8'))

# Append to a string
redis_client.append('my_string', ' How are you?')
value = redis_client.get('my_string')
print(value.decode('utf-8'))

