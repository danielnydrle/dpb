import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.flushall()

# 5 záznamů
r.set('name', 'John')
r.set('age', 30)
r.set('city', 'New York')
r.set('country', 'USA')
r.set('email', 'john.doe@gmail.com')

# existence klíče
print("exists name: " + str(r.exists('name')))

# jeden ze záznamů
print(r.get('name'))

# jeden ze záznamů aktualizovat
r.set('name', 'John Doe')

# jeden ze záznamů smazat
r.delete('email')

# jeden ze záznamů smazat za 60 sekund
r.expire('city', 60)

# během těch 60 vteřin zjistit zbývající čas
time.sleep(4)
print(r.ttl('city'))
