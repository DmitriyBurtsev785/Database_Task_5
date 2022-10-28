
import psycopg2


def create_db(conn):

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


def add_client(conn, name, surname, email, phones=None):

    cur.execute("""
    INSERT INTO client_management(name, surname, email) VALUES(%s, %s, %s);
    """, (name, surname, email))


def add_phone(conn, phone, client_management_id):

    cur.execute("""
    INSERT INTO phones(phone, client_management_id) VALUES(%s, %s);
    """, (phone, client_management_id))


def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):

    cur.execute("""
    UPDATE client_management SET name=%s, surname=%s, email=%s  WHERE id=%s;
    """, (name, surname, email, client_id))


def change_client_name(conn, client_id, name=None):

    cur.execute("""
    UPDATE client_management SET name=%s  WHERE id=%s;
    """, (name, client_id))

def change_client_surname(conn, client_id, surname=None):

    cur.execute("""
    UPDATE client_management SET surname=%s  WHERE id=%s;
    """, (surname, client_id))

def change_client_email(conn, client_id, email=None):

    cur.execute("""
    UPDATE client_management SET email=%s  WHERE id=%s;
    """, (email, client_id))



def delete_phone(conn, client_id, phone):

    cur.execute("""
    DELETE FROM phones WHERE id=%s;
    """, (client_id,))


def delete_client(conn, client_id):

    cur.execute("""
    DELETE FROM phones WHERE client_management_id=%s;
    """, (client_id,))

    cur.execute("""
    DELETE FROM client_management WHERE id=%s;
    """, (client_id,))


def find_client(conn, name=None, surname=None, email=None, phone=None):

    cur.execute("""
    SELECT id, name, surname, email FROM client_management WHERE name=%s or surname=%s or email=%s;
    """, (name, surname, email))
    a = cur.fetchone()
    print(a)

    cur.execute("""
    SELECT id, phone, client_management_id FROM phones WHERE client_management_id=%s;
    """, (a[0], ))
    print(cur.fetchone())


def find_client_2(conn, phone=None):


    cur.execute("""
    SELECT id, phone, client_management_id FROM phones WHERE phone=%s;
    """, (phone, ))
    a = cur.fetchone()
    print(a)

    cur.execute("""
    SELECT id, name, surname, email FROM client_management WHERE id=%s;
    """, (a[2],))
    print(cur.fetchone())


def test(conn, name=None, surname=None, email=None, phone=None):

    cur.execute("""
    SELECT * FROM client_management;
    """)
    print(cur.fetchall())


def test_2(conn):

    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())





if __name__ == "__main__":



    with psycopg2.connect(database="client_management", user="postgres", password="Lvbnhbq1985") as conn:


        with conn.cursor() as cur:

# удаление таблиц

            cur.execute("""
            DROP TABLE phones;
            DROP TABLE client_management;
            """)

# 1. Функция, создающая структуру БД (таблицы)

            create_db(conn)

# 2. Функция, позволяющая добавить нового клиента

            add_client(conn, 'Иван', 'Иванов', 'ivanov@abc.com')
            add_client(conn, 'Сергей', 'Сергеев', 'sergeev@abc.com')
            add_client(conn, 'Семен', 'Семёнов', 'semenov@abc.com')
            add_client(conn, 'Егор', 'Егоров', 'egorov@abc.com')
            add_client(conn, 'Антон', 'Антонов', 'antonov@abc.com')
#
# # 3. Функция, позволяющая добавить телефон для существующего клиента

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
            change_client_name(conn, 1, 'Игнат')
            change_client_surname(conn, 1, 'Игнатов')
            change_client_email(conn, 1, 'ignatov@abc.com')


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

            find_client(conn, 'Сергей', 'Сергеев', 'sergeev@abc.com', '88882223344')
            find_client(conn, 'Сергей', 'Сергеев', 'sergeev@abc.com')
            find_client(conn, 'Сергей', 'Сергеев')
            find_client(conn, 'Сергей')
            find_client(conn, '', '', 'sergeev@abc.com')
            find_client(conn, '' ,'Игнатов', '')
            find_client(conn, '' ,'Игнатов', 'ignatov@abc.com')


# 8. Функция, позволяющая найти клиента по его данным (телефону)

            find_client_2(conn, '88882223344')
            find_client_2(conn, '83335557766')


    conn.close()