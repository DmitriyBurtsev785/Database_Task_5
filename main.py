

import psycopg2

# удаление таблиц
with psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phones;
        DROP TABLE client_management;
        """)


def create_db(conn):

    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client_management(
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            surname VARCHAR(30) NOT NULL,
            email VARCHAR(40) UNIQUE
            );
            """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR(12) UNIQUE,
            client_management_id INTEGER REFERENCES client_management(id)
            );
            """)
    conn.commit()  # фиксируем в БД


def add_client(conn, name, surname, email, phones=None):
    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client_management(name, surname, email) VALUES(%s, %s, %s);
        """, (name, surname, email))
        conn.commit()


def add_phone(conn, phone, client_management_id):
    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones(phone, client_management_id) VALUES(%s, %s);
        """, (phone, client_management_id))

        conn.commit()


def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client_management SET name=%s, surname=%s, email=%s  WHERE id=%s;
        """, (name, surname, email, client_id))

        conn.commit()


def delete_phone(conn, client_id, phone):
    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:

        cur.execute("""
        DELETE FROM phones WHERE id=%s;
        """, (client_id,))

        conn.commit()


def delete_client(conn, client_id):

    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:

        cur.execute("""
        DELETE FROM phones WHERE client_management_id=%s;
        """, (client_id,))

        conn.commit()

        cur.execute("""
        DELETE FROM client_management WHERE id=%s;
        """, (client_id,))

        conn.commit()


def find_client_2(conn, name=None, surname=None, email=None, phone=None):

    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:


        # cur.execute("""
        # SELECT id, name, surname, email FROM client_management WHERE name='name' and surname='surname' and email='email';
        # """)
        # print(cur.fetchone())
        # print(name, surname, email)


        cur.execute("""
        SELECT id, name, surname, email FROM client_management WHERE name=%s or surname=%s or email=%s;
        """, (name, surname, email))  # хорошо, обратите внимание на кортеж
        print(cur.fetchone())

        cur.execute("""
        SELECT id, phone, client_management_id FROM phones WHERE phone=%s;
        """, (phone, ))  # хорошо, обратите внимание на кортеж
        print(cur.fetchone())


def test(conn, name=None, surname=None, email=None, phone=None):
    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:

        cur.execute("""
        SELECT * FROM client_management;
        """)
        print(cur.fetchall())


def test_2(conn):
    conn = psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985")
    with conn.cursor() as cur:

        cur.execute("""
        SELECT * FROM phones;
        """)
        print(cur.fetchall())


with psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985") as conn:



# 1. Функция, создающая структуру БД (таблицы)

    create_db(conn)

# 2. Функция, позволяющая добавить нового клиента

    add_client(conn, 'Иван', 'Иванов', 'ivanov@abc.com')
    add_client(conn, 'Сергей', 'Сергеев', 'sergeev@abc.com')
    add_client(conn, 'Семен', 'Семёнов', 'semenov@abc.com')
    add_client(conn, 'Егор', 'Егоров', 'egorov@abc.com')
    add_client(conn, 'Антон', 'Антонов', 'antonov@abc.com')

# 3. Функция, позволяющая добавить телефон для существующего клиента

    add_phone(conn, '89995552244', 1)
    add_phone(conn, '89995551122', 1)
    add_phone(conn, '88882223344', 2)
    add_phone(conn, '89896669955', 2)
    add_phone(conn, '80007771144', 3)
    add_phone(conn, '81114447799', 4)
    add_phone(conn, '83335557766', 5)
    add_phone(conn, '84446661199', 5)


# тест (проверка, что клиенты и номера телефонов успешно добавлены)

    test(conn)

    test_2(conn)


# 4. Функция, позволяющая изменить данные о клиенте

    change_client(conn, 1, 'Пётр', 'Петров', 'petrov@abc.com')


# тест (проверка, что данные о клиенте изменены)

    test(conn)

# 5. Функция, позволяющая удалить телефон для существующего клиента

    delete_phone(conn, 1, '89995552244')

# тест (номер телефона успешно удалён)

    test_2(conn)


# 6. Функция, позволяющая удалить существующего клиента

    delete_client(conn, 4)

# тест (клиент и его контакты удалены)

    test(conn)
    test_2(conn)

# 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)


    find_client_2(conn, 'Сергей', 'Сергеев', 'sergeev@abc.com', '88882223344')
    find_client_2(conn, 'Сергей', 'Сергеев', 'sergeev@abc.com')
    find_client_2(conn, 'Сергей', 'Сергеев')
    find_client_2(conn, 'Сергей')

    find_client_2(conn, '111', '222', '333@abc.com')


conn.close()