import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def update_leaderboard(restaurant_id, score):
    r.zincrby("restaurant_leaderboard", score, str(restaurant_id))

def get_leaderboard(top_n=10):
    return r.zrevrange("restaurant_leaderboard", 0, top_n-1, withscores=True)
