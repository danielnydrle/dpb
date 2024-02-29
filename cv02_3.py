import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.flushall()

# každý hráč má mít jméno a skóre (od 0 do 999)
# 1. hráč Alfred (888 vodů)
r.zadd('leaderboard', {'Alfred': 888})

# přidat dalších 10 hráčů
r.zadd('leaderboard', {'John': 50})
r.zadd('leaderboard', {'Jane': 200})
r.zadd('leaderboard', {'Mike': 300})
r.zadd('leaderboard', {'Anna': 400})
r.zadd('leaderboard', {'Tom': 500})
r.zadd('leaderboard', {'Jerry': 600})
r.zadd('leaderboard', {'Mia': 700})
r.zadd('leaderboard', {'Eva': 800})
r.zadd('leaderboard', {'Peter': 899})
r.zadd('leaderboard', {'Paul': 999})

# vypsat 3 nejlepší hráče a jejich skóre
print(r.zrevrange('leaderboard', 0, 2))
# nebo
print(r.zrange('leaderboard', 0, 2, desc=True))

# zjistit nejhorší skóre
print(r.zscore('leaderboard', r.zrange('leaderboard', 0, 0)[0]))

# zjistit počet hráčů s méně než 100 body
print(r.zcount('leaderboard', 0, 99))

# zjistit všechny hráče s více než 850 body
print(r.zrangebyscore('leaderboard', 850, 999))

# zjistit Alfredovu pozici v žebříčku
print(r.zrevrank('leaderboard', 'Alfred') + 1)

# inkrementovat skóre Alfreda o 12 a zjistit jeho novou pozici
r.zincrby('leaderboard', 12, 'Alfred')
print(r.zrevrank('leaderboard', 'Alfred') + 1)
