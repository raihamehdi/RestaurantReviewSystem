import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def update_leaderboard(restaurant_id, score):
    r.zincrby("restaurant_leaderboard", score, restaurant_id)

def get_leaderboard():
    return r.zrevrange("restaurant_leaderboard", 0, 9, withscores=True)
