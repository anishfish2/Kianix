import redis
import sys

def main(action):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set("current_action", action)

    
if __name__ == "__main__":
    action = sys.argv[1]
    main(action)
    