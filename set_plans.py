import redis
import sys

def main(plan):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set("plans", plan)

    
if __name__ == "__main__":
    plan = sys.argv[1]
    main(plan)
    