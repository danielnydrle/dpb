import datetime
from init import collection

'''
DPB - 5. Cvičení

Implementujte jednotlivé body pomocí PyMongo knihovny - rozhraní je téměř stejné jako v Mongo shellu.
Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru.

Pro pomoc je možné např. použít https://www.w3schools.com/python/python_mongodb_getstarted.asp

Funkce find vrací kurzor - pro vypsání výsledku je potřeba pomocí foru iterovat nad kurzorem:

cursor = collection.find(...)
for restaurant in cursor:
    print(restaurant) # případně print(restaurant['name'])

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


def print_restaurants(cursor):
    for r in cursor:
        print(r)


def print_restaurant_names(cursor):
    for rn in cursor:
        print(rn["name"])


# 1. Vypsání všech restaurací
print_delimiter(1)
cursor = collection.find()
print_restaurants(cursor)

# 2. Vypsání všech restaurací - pouze názvů, abecedně seřazených
print_delimiter(2)
cursor = collection.find({}, {"name": 1, "_id": 0}).sort(
    key_or_list="name", direction=1)
print_restaurant_names(cursor)

# 3. Vypsání pouze 5 záznamů z předchozího dotazu
print_delimiter(3)
cursor = collection.find({}, {"name": 1, "_id": 0}).sort(
    key_or_list="name", direction=1
).limit(5)
print_restaurant_names(cursor)

# 4. Zobrazte dalších 10 záznamů
print_delimiter(4)
cursor = collection.find({}, {"name": 1, "_id": 0}).sort(
    key_or_list="name", direction=1
).skip(10).limit(5)
print_restaurant_names(cursor)

# 5. #Vypsání restaurací ve čtvrti Bronx (čtvrť = borough)
print_delimiter(5)
cursor = collection.find({"borough": "Bronx"})
print_restaurants(cursor)

# 6. Vypsání restaurací, jejichž název začíná na písmeno M
print_delimiter(6)
cursor = collection.find({"name": {"$regex": "^M"}})
print_restaurants(cursor)

# 7. Vypsání restaurací, které mají skóre větší než 80
print_delimiter(7)
cursor = collection.find({"grades.score": {"$gt": 80}})
print_restaurants(cursor)

# 8. Vypsání restaurací, které mají skóre mezi 80 a 90
print_delimiter(8)
cursor = collection.find(
    {"grades": {"$elemMatch": {"score": {"$gte": 80, "$lte": 90}}}})
print_restaurants(cursor)

'''
Bonusové úlohy:
'''

# 9. Vypsání všech restaurací, které mají skóre mezi 80 a 90 a zároveň nevaří americkou (American) kuchyni
print_delimiter(9)
cursor = collection.find(
    {"grades": {"$elemMatch": {"score": {"$gte": 80, "$lte": 90}}}, "cuisine": {"$ne": "American"}})
print_restaurants(cursor)

# 10. Vypsání všech restaurací, které mají alespoň osm hodnocení
print_delimiter(10)
cursor = collection.find({"grades.7": {"$exists": True}})
print_restaurants(cursor)

# 11. Vypsání všech restaurací, které mají alespoň jedno hodnocení z roku 2014
print_delimiter(11)
cursor = collection.find({"grades.date": {"$gte": datetime.datetime(
    2014, 1, 1), "$lt": datetime.datetime(2015, 1, 1)}})
print_restaurants(cursor)

'''
V této části budete opět vytvářet vlastní restauraci.

Řešení:
Vytvořte si vaši restauraci pomocí slovníku a poté ji vložte do DB.
restaurant = {
    ...
}
'''

# 12. Uložte novou restauraci (stačí vyplnit název a adresu)
print_delimiter(12)
restaurant = {
    "name": "Restaurace 123",
    "address": {
        "street": "Ulice 123"
    }
}
collection.insert_one(restaurant)

# 13. Vypište svoji restauraci
print_delimiter(13)
cursor = collection.find({"name": "Restaurace 123"})
print_restaurants(cursor)

# 14. Aktualizujte svoji restauraci - změňte libovolně název
print_delimiter(14)
collection.update_one({"name": "Restaurace 123"}, {
    "$set": {"name": "Restaurace 456"}})

print("Pocet restauraci 123/456:", collection.find(
    {"$or": [{"name": "Restaurace 123"}, {"name": "Restaurace 456"}]}).count())

# 15. Smažte svoji restauraci
# 15.1 pomocí id (delete_one)
# 15.2 pomocí prvního nebo druhého názvu (delete_many, využití or)
print_delimiter(15)

# 15.1
collection.delete_one({"name": "Restaurace 456"})
# 15.2
collection.delete_many(
    {"$or": [{"name": "Restaurace 123"}, {"name": "Restaurace 456"}]})

print("Pocet restauraci 123/456:", collection.find(
    {"$or": [{"name": "Restaurace 123"}, {"name": "Restaurace 456"}]}).count())

'''
Poslední částí tohoto cvičení je vytvoření jednoduchého indexu.

Použijte např. 3. úlohu s vyhledáváním čtvrtě Bronx. První použijte Váš již vytvořený dotaz a na výsledek použijte:

cursor.explain()['executionStats'] - výsledek si vypište na výstup a všimněte si položky 'totalDocsExamined'

Poté vytvořte index na 'borough', zopakujte dotaz a porovnejte hodnoty 'totalDocsExamined'.

S řešením pomůže https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index
'''
print_delimiter(11)

cursor = collection.find({"borough": "Bronx"})
print(cursor.explain()['executionStats'])

collection.create_index("borough")
cursor = collection.find({"borough": "Bronx"})
print(cursor.explain()['executionStats'])
