from init import collection

'''
DPB - 6. cvičení - Agregační roura a Map-Reduce

V tomto cvičení si můžete vybrat, zda ho budete řešit v Mongo shellu nebo pomocí PyMongo knihovny.

Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru - používáme stejná data jako v minulých cvičeních.

Pro pomoc je možné např. použít https://api.mongodb.com/python/current/examples/aggregation.html a přednášku.

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!

Struktura záznamu v db:
{
  "address": {
     "building": "1007",
     "coord": [ -73.856077, 40.848447 ],
     "street": "Morris Park Ave",
     "zipcode": "10462"
  },
  "borough": "Bronx",
  "cuisine": "Bakery",
  "grades": [
     { "date": { "$date": 1393804800000 }, "grade": "A", "score": 2 },
     { "date": { "$date": 1378857600000 }, "grade": "A", "score": 6 },
     { "date": { "$date": 1358985600000 }, "grade": "A", "score": 10 },
     { "date": { "$date": 1322006400000 }, "grade": "A", "score": 9 },
     { "date": { "$date": 1299715200000 }, "grade": "B", "score": 14 }
  ],
  "name": "Morris Park Bake Shop",
  "restaurant_id": "30075445"
}
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


'''
Agregační roura
Zjistěte počet restaurací pro každé PSČ (zipcode)
 a) seřaďte podle zipcode vzestupně
 b) seřaďte podle počtu restaurací sestupně
Výpis limitujte na 10 záznamů a k provedení použijte collection.aggregate(...)
'''

print_delimiter('1 a)')
cursor = collection.aggregate([
    # {"$match": {"address.zipcode": {"$ne": ""}}},
    {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}},
    {"$limit": 10}
])

for c in cursor:
    print(c)


print_delimiter('1 b)')
cursor = collection.aggregate([
    {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])

for c in cursor:
    print(c)

print_delimiter(1)

'''
Agregační roura

Restaurace obsahují pole grades, kde jsou jednotlivá hodnocení. Vypište průměrné score pro každou hodnotu grade.
V agregaci vynechte grade pro hodnotu "Not Yet Graded" (místo A, B atd. se může vyskytovat tento řetězec).

'''
print_delimiter(2)

cursor = collection.aggregate([
    {"$unwind": "$grades"},
    {"$match": {"grades.grade": {"$ne": "Not Yet Graded"}}},
    {"$group": {"_id": "$grades.grade", "avg_score": {"$avg": "$grades.score"}}}
])

for c in cursor:
    print(c)

print_delimiter("bonus 1")

# zjistěte 5 restaurací s nejlepším průměrným skóre pro známku A
# restaurace s méně než třemi hodnoceními nebudou uvažovány
# ve výsledku vypisuje kromě průměrného skóre i počet hodnocení
# úlohu vyřešte pomocí agregační roury

cursor = collection.aggregate([
    {"$unwind": "$grades"},
    {"$match": {"grades.grade": "A"}},
    {"$group": {"_id": "$name", "avg_score":
                {"$avg": "$grades.score"},
                "count": {"$sum": 1}}, },
    {"$match": {"count": {"$gte": 3}}},
    {"$sort": {"avg_score": -1}},
    {"$limit": 5}
])

for c in cursor:
    print(c)

print_delimiter("bonus 2")
# nalezněte nejlepší restauraci pro každý typ kuchyně
# rozšiřte předchozí úlohu
# úlohu vyřešte pomocí agregační roury

cursor = collection.aggregate([
    {"$unwind": "$grades"},
    {"$match": {"grades.grade": "A"}},
    {"$group": {"_id": {"name": "$name", "cuisine": "$cuisine"},
                "avg_score": {"$avg": "$grades.score"}, "count": {"$sum": 1}},
     },
    {"$match": {"count": {"$gte": 3}}},
    {"$sort": {"avg_score": -1}},
    {"$group": {"_id": "$_id.cuisine", "name": {
        "$first": "$_id.name"}, "avg_score": {"$first": "$avg_score"}}}
])

for c in cursor:
    print(c)

print_delimiter("bonus 3")
cursor = collection.aggregate([
    {"$match": {"name": {"$regex": ".* .*"}}},
    {"$unwind": "$grades"},
    {"$match": {"grades.score": {"$gte": 10}}},
    {"$group": {"_id": "$name", "count": {"$sum": 1}},
     },
    {"$match": {"count": {"$gte": 2}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])

for c in cursor:
    print(c)
