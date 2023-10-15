import redis

redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)

while True:
    if input() == "a":
        print(redis_server.lpop("twitch_chat"))

