import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

r.set('my_key', 'initial_value')

value = r.get('my_key')

if value != None:
    decoded_value = value.decode('utf-8')
    print(decoded_value)
else:
    print("Key not found")

r.set('my_key', 'new_value')

value = r.get('my_key')

if value != None:
    decoded_value = value.decode('utf-8')
    print(decoded_value)
else:
    print("Key not found")