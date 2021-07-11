import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

"""
Пример нативной работы Python с SQL, используя библиотеку psycopg2
"""

# параметры соединения с базой данных dbname имя базы, user СУБД postgres, password пароль к базе, host, port
connect = psycopg2.connect(dbname="test_db", user="postgres", password='')

# позволяет коду Python выполнять команду PostgreSQL в сеансе базы данных
cur = connect.cursor()

# используя запрос DROP можно удалить таблицы TABLE, индексы INDEX и базы данных DATABASE
cur.execute("DROP TABLE IF EXISTS superheroes;")
cur.execute("DROP TABLE IF EXISTS traffic_light;")

# этот метод отправляет COMMIT запрос серверу PostgresSQL, фиксируя текущую транзакцию
connect.commit()

# оператор CREATE TABLE используется для создания новой таблицы в базе данных
cur.execute("CREATE TABLE superheroes (hero_id serial PRIMARY KEY, hero_name varchar, strength int);")

# оператор INSERT INTO используется для вставки новых записей в таблицу
# также символы %s позволяют передавать параметры безопасно, второй аргумент кортеж (tuple)
cur.execute("INSERT INTO superheroes (hero_name, strength) VALUE (%s, %s);", ("Superman", 100))

# еще один вариант передачи данных используя словарь (dict)
cur.execute("""
                INSERT INTO superheroes (hero_name, strength)
                VALUE (%(name)s, %(strength)s);
            """, {'name': 'Green Arrow', 'strength': 80})

connect.commit()

cur.execute("CREATE TABLE traffic_light (light_id serial PRIMARY KEY, light text);")

cur.execute("INSERT INTO traffic_light (light) VALUE (%s);", ('red',))

one_line = cur.fetchone()
print(one_line)

full_fetch = cur.fetchall()
for record in full_fetch:
    print(record)

connect.commit()

cur.close()
connect.close()

# еще вариант работы с базой данных для предотвращения перегруженности соединения слишком долго открытой транзакцией
with psycopg2.connect(dbname="test_db", user="postgres", password='') as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        # передача множества данных выполняется значительно бытрее одним запросом
        execute_values(curs, "INSERT INTO traffic_light (light) VALUE (%s);", [('red',), ('yellow',)])

        curs.execute("SELECT * FROM traffic_light")
        records = curs.fetchall()
        print(records)
        print(records[0]["light"])

# данный вариант также можно использовать в рамкаж одно with чтобы работать с соединением более одно раза
connect = psycopg2.connect(dbname="test_db", user="postgres", password='')
try:
    with connect:
        with connect.cursor() as cur:
            curs.execute("""
                        UPDATE superheroes
                        SET strength = %s
                        WHERE hero_name = %s
                        """, (90, "Superman"))

    with connect:
        with connect.cursor() as cur:
            curs.execute("SELECT * FROM traffic_light")
            print(curs.fetchall())
finally:
    # закрываем соединение явно
    connect.close()
