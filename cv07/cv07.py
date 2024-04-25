from elasticsearch import Elasticsearch

INDEX_NAME = 'person'


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


USERNAME = "elastic"
PASSWORD = "elastic"

# Připojení k ES
es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, "scheme": "https"}],
                   http_auth=(USERNAME, PASSWORD),
                   ssl_show_warn=False,
                   verify_certs=False
                   )

# Kontrola zda existuje index 'person'
if not es.indices.exists(index=INDEX_NAME):
    # Vytvoření indexu
    es.indices.create(index=INDEX_NAME)

# Index není potřeba vytvářet - pokud neexistuje, tak se automaticky vytvoří při vložení prvního dokumentu

# delete all documents in INDEX_NAME
es.delete_by_query(index=INDEX_NAME, body={"query": {"match_all": {}}})

# 1. Vložte osobu se jménem John
print_delimiter(1)
person = {
    "name": "John"
}
response = es.create(index=INDEX_NAME, body=person, id=1)
# nebo
response = es.index(index=INDEX_NAME, body=person)

# 2. Vypište vytvořenou osobu (pomocí get a parametru id)
print_delimiter(2)
response = es.get(index=INDEX_NAME, id=1)
print(response['_source'])

# 3. Vypište všechny osoby (pomocí search)
print_delimiter(3)
response = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}})
for hit in response['hits']['hits']:
    print(hit['_source'])

# 4. Přejmenujte vytvořenou osobu na 'Jane'
print_delimiter(4)
response = es.update(index=INDEX_NAME, id=1, body={
                     "doc": {"name": "Jane"}})

response = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}})
for hit in response['hits']['hits']:
    print(hit['_source'])

# 5. Smažte vytvořenou osobu
print_delimiter(5)
response = es.delete(index=INDEX_NAME, id=1)

response = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}})
for hit in response['hits']['hits']:
    print(hit['_source'])

# 6. Smažte vytvořený index
print_delimiter(6)
response = es.indices.delete(index=INDEX_NAME)
