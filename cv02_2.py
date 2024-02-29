import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.flushall()

# do seznamu todolist několik úkolů - na konec
r.rpush('todolist', 'ukol1')
r.rpush('todolist', 'ukol2')
r.rpush('todolist', 'ukol3')
r.rpush('todolist', 'ukol4')
r.rpush('todolist', 'ukol5')

# vložit úkol na začátek seznamu
r.lpush('todolist', 'ukol0')

# vypsat všechny úkoly
print(r.lrange('todolist', 0, -1))

# vypsat počet úkolů
print(r.llen('todolist'))

# "dokončit" vybraný úkol - přesunout do seznamu 'finished'
r.lrem('todolist', 1, 'ukol3')
r.rpush('finished', 'ukol3')

# vypsat všechny úkoly
print(r.lrange('todolist', 0, -1))
print(r.lrange('finished', 0, -1))
