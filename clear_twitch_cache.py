import redis

def clear_redis_list(host='localhost', port=6379, db=0, key='twitch_chat'):
    try:

        r = redis.StrictRedis(host=host, port=port, db=db)

        r.ltrim(key, 1, 0) 

        print(f"List under key '{key}' cleared successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clear_redis_list()
