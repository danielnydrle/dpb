import csv
from cassandra.cluster import Cluster
import time


# DPB - 11. cvičení Cassandra

# Use case: Discord server - reálně používáno pro zprávy, zde pouze zjednodušená varianta.

# Instalace python driveru: pip install cassandra-driver

# V tomto cvičení se budou následující úlohy řešit s využitím DataStax driveru pro Cassandru.
# Dokumentaci lze nalézt zde: https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/


# Optimální řešení (nepovinné) - pokud něco v db vytváříme, tak první kontrolujeme, zda to již neexistuje.


# Pro uživatele PyCharmu:

# Pokud chcete zvýraznění syntaxe, tak po napsání prvního dotazu se Vám u něj objeví žlutá žárovka, ta umožňuje vybrat
# jazyk pro tento projekt -> vyberte Apache Cassandra a poté Vám nabídne instalaci rozšíření pro tento typ db.
# Zvýraznění občas nefunguje pro příkaz CREATE KEYSPACE.

# Také je možné do PyCharmu připojit databázi -> v pravé svislé liště najděte Database a připojte si lokální Cassandru.
# Řešení cvičení chceme s využitím DataStax driveru, ale s integrovaným nástrojem pro databázi si můžete pomoct sestavit
# příslušně příkazy.


# Pokud se Vám nedaří připojit se ke Cassandře v Dockeru, zkuste smazat kontejner a znovu spustit:

# docker run --name dpb_cassandra -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d cassandra:latest


def print_delimiter(n):
    """Vytiskne oddělovač pro jednotlivé úlohy."""
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


def print_result(result):
    """Vytiskne výsledek dotazu."""
    for r in result:
        print(r)


cluster = Cluster()  # automaticky se připojí k localhostu na port 9042
session = cluster.connect()

"""
1. Vytvořte keyspace 'dc' a přepněte se do něj (SimpleStrategy, replication_factor 1)
"""

print_delimiter(1)

CREATE_KEYSPACES = """
CREATE KEYSPACE IF NOT EXISTS dc
WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
"""

session.execute(CREATE_KEYSPACES)

session.execute("USE dc;")

# session.set_keyspace('dc')


# 2. V csv souboru message_db jsou poskytnuta data pro cvičení. V prvním řádku naleznete názvy sloupců.
#    Vytvořte tabulku messages - zvolte vhodné datové typy (time bude timestamp)
#    Primárním klíčem bude room_id a time
#    Data chceme mít seřazené podle času, abychom mohli rychle získat poslední zprávy

#    Jako id v této úloze zvolíme i time - zdůvodněte, proč by se v praxi time jako id neměl používat.

#    Pokud potřebujeme použít čas, tak se v praxi používá typ timeuuid nebo speciální identifikátor, tzv. Snowflake ID
#    (https://en.wikipedia.org/wiki/Snowflake_ID). Není potřeba řešit v tomto cvičení.


print_delimiter(2)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    room_id INT,
    speaker_id INT,
    time TIMESTAMP,
    message TEXT,
    PRIMARY KEY (room_id, time)
) WITH CLUSTERING ORDER BY (time DESC);
"""

session.execute(CREATE_TABLE)


# 3. Do tabulky messages importujte message_db.csv
#    COPY není možné spustit pomocí DataStax driveru('copy' is a cqlsh(shell) command rather than a CQL(protocol) command)
#    -> 2 možnosti:
#       a) Nakopírovat csv do kontejneru a spustit COPY příkaz v cqlsh konzoli uvnitř dockeru
#       b) Napsat import v Pythonu - otevření csv a INSERT dat
# CSV soubor může obsahovat chybné řádky - COPY příkaz automaticky přeskočí řádky, které se nepovedlo správně parsovat


print_delimiter(3)


def import_csv():
    """Importuje data z csv souboru do tabulky messages."""
    with open('cv11/message_db.csv', 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # přeskočení hlavičky
        for r in reader:
            vals = r[0].split(";")
            session.execute(
                """
                INSERT INTO messages (room_id, speaker_id, time, message)
                VALUES (%s, %s, %s, %s)
                """,
                (int(vals[0]), int(vals[1]), vals[2], vals[3])
            )


# import_csv()


# 4. Kontrola importu - vypište 1 zprávu


print_delimiter(4)

SELECT_MESSAGE = """
SELECT * FROM messages LIMIT 1;
"""

print_result(session.execute(SELECT_MESSAGE))


# 5. Vypište posledních 5 zpráv v místnosti 1 odeslaných uživatelem 2
#     Nápověda 1: Sekundární index(viz přednáška)
#     Nápověda 2: Data jsou řazena již při vkládání


print_delimiter(5)

CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS speaker_idx ON messages (speaker_id);
"""

SELECT_LAST_MESSAGES = """
SELECT * FROM messages WHERE room_id = 1 AND speaker_id = 2 LIMIT 5;
"""

session.execute(CREATE_INDEX)

print_result(session.execute(SELECT_LAST_MESSAGES))


# 6. Vypište počet zpráv odeslaných uživatelem 2 v místnosti 1


print_delimiter(6)

SELECT_COUNT_MESSAGES = """
SELECT COUNT(*) FROM messages WHERE room_id = 1 AND speaker_id = 2;
"""

print_result(session.execute(SELECT_COUNT_MESSAGES))


# 7. Vypište počet zpráv v každé místnosti


print_delimiter(7)

SELECT_COUNT_MESSAGES_ROOM = """
SELECT room_id, COUNT(*) FROM messages GROUP BY room_id;
"""

print_result(session.execute(SELECT_COUNT_MESSAGES_ROOM))


# 8. Vypište id všech místností(3 hodnoty)


print_delimiter(8)

SELECT_ROOM_IDS = """
SELECT DISTINCT room_id FROM messages;
"""

print_result(session.execute(SELECT_ROOM_IDS))


# Bonusové úlohy:

# 1. Pro textovou analýzu chcete poskytovat anonymizovaná textová data. Vytvořte Materialized View pro tabulku messages,
# který bude obsahovat pouze čas, room_id a zprávu.

# Vypište jeden výsledek z vytvořeného view

# Před začátkem řešení je potřeba jít do souboru cassandra.yaml uvnitř docker kontejneru a nastavit enable_materialized_views = true

# docker exec - it dpb_cassandra bash
# sed -i -r 's/materialized_views_enabled: false/materialized_views_enabled: true/' /etc/cassandra/cassandra.yaml

# Poté restartovat kontejner


print_delimiter('Bonus 1')

CREATE_MV = """
CREATE MATERIALIZED VIEW IF NOT EXISTS messages_anonymized AS
SELECT room_id, time, message
FROM messages
WHERE room_id IS NOT NULL AND time IS NOT NULL AND message IS NOT NULL
PRIMARY KEY (room_id, time)
WITH CLUSTERING ORDER BY (time DESC);
"""

SELECT_MV = """
SELECT * FROM messages_anonymized LIMIT 1;
"""

print_result(session.execute(SELECT_MV))


# 2. Chceme vytvořit funkci(UDF), která při výběru dat vrátí navíc příznak, zda vybraný text obsahuje nevhodný výraz.

# Vyberte jeden výraz (nemusí být nevhodný: ), vytvořte a otestujte Vaši funkci.

# Potřeba nastavit enable_user_defined_functions = true v cassandra.yaml

# sed -i -r 's/user_defined_functions_enabled: false/user_defined_functions_enabled: true/' /etc/cassandra/cassandra.yaml


print_delimiter('Bonus 2')

CHECK_BAD_WORD = """
    CREATE OR REPLACE FUNCTION check_inappropriate(text_value text)
    CALLED ON NULL INPUT
    RETURNS text
    LANGUAGE java
    AS '
        if (text_value.contains("from")) {
            return "X";
        }
        return "O";
    ';
"""

SELECT_BAD_WORD = """
SELECT message, check_inappropriate(message) FROM messages LIMIT 2;
"""

print_result(session.execute(SELECT_BAD_WORD))


# 3. Zjistěte čas odeslání nejnovější a nejstarší zprávy.


print_delimiter('Bonus 3')

SELECT_MIN_MAX_TIME = """
SELECT MIN(time), MAX(time) FROM messages;
"""

print_result(session.execute(SELECT_MIN_MAX_TIME))


# 4. Zjistěte délku nejkratší a nejdelší zprávy na serveru.


print_delimiter('Bonus 4')

session.execute(
    """
        CREATE FUNCTION IF NOT EXISTS LENGTH (input text) 
        CALLED ON NULL INPUT 
        RETURNS int 
        LANGUAGE java AS '
            return input.length();
        ';
    """
)

SELECT_MIN_MAX_LENGTH = """
SELECT MIN(LENGTH(message)), MAX(LENGTH(message)) FROM messages;
"""

print_result(session.execute(SELECT_MIN_MAX_LENGTH))


# 5. Pro každého uživatele zjistěte průměrnou délku zprávy.


print_delimiter('Bonus 5')

SELECT_USER_MESSAGES = """
SELECT speaker_id, LENGTH(message) as length FROM messages;
"""
data = {}

for row in session.execute(SELECT_USER_MESSAGES):
    data[row.speaker_id] = data.get(row.speaker_id, []) + [row.length]

for speaker_id, lengths in sorted(data.items()):
    print(f"Speaker {speaker_id}: {sum(lengths) / len(lengths)}")
