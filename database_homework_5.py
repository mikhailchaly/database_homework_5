import psycopg2
from pprint import pprint

def client_data(cur):
    # таблица данных клиентов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client_data(
        client_id  SERIAL PRIMARY KEY,
        client_name VARCHAR(30) NOT NULL,
        client_surname VARCHAR(30) NOT NULL,
        client_email VARCHAR(30) NOT NULL);
    """)

    # таблица телефонов клиентов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS numbers_phone(
        phon_id SERIAL PRIMARY KEY,
        client_phone_id INTEGER NOT NULL REFERENCES client_data(client_id),
        client_number_phone VARCHAR(20) UNIQUE);
    """)

def add_data_client(cur, client_name, client_surname, client_email):
    cur.execute("""
        INSERT INTO client_data(client_name, client_surname, client_email) VALUES(%s, %s, %s);
    """, (client_name, client_surname, client_email))

def add_number_phone(cur, client_phone_id, client_number_phone):
    cur.execute("""
        INSERT INTO numbers_phone(client_phone_id, client_number_phone) VALUES (%s, %s);
    """, (client_phone_id, client_number_phone))

def change_data_client():
    print("изменить имя - 1\nизменить фамилия - 2\nизменить email - 3"
          "\nизменить номер телефона - 4\nвыйти и сохранить - 0")
    while True:
        input_command = int(input("_ "))
        if input_command not in [1, 2, 3, 4, 0]:
            print("нет такой команды")
            return change_data_client()
        elif input_command == 0:
            break
        else:
            if input_command == 1:
                input_id = input("Введи id клиента ")
                input_name = input('Введи новое имя ')
                cur.execute("""
                    UPDATE client_data SET client_name=%s WHERE client_id=%s;
                    """, (input_name, input_id))
            elif input_command == 2:
                input_id = input("Введи id клиента ")
                input_surname = input('Введи новую фамилию ')
                cur.execute("""
                    UPDATE client_data SET client_surname=%s WHERE client_id=%s;
                """, (input_surname, input_id))
            elif input_command == 3:
                input_id = input("Введи id клиента ")
                input_email = input('Введи новый email ')
                cur.execute("""
                    UPDATE client_data SET client_email=%s WHERE client_id=%s;
                """, (input_email, input_id))
            elif input_command == 4:
                input_old_number_phone = input("Введи номер телефона, который заменить ")
                input_new_number_phone = input('Введи новый номер телефона ')
                cur.execute("""
                    UPDATE numbers_phone SET client_number_phone=%s WHERE client_number_phone=%s;
                """, (input_new_number_phone, input_old_number_phone))

def delete_phone_client(cur):
    input_id = input("Введи id клиента ")
    input_number_phone = input('Введи номер телефона для удаления ')
    cur.execute("""
    DELETE FROM numbers_phone WHERE client_phone_id=%s AND client_number_phone=%s
    """, (input_id, input_number_phone))

def delete_client_data(cur):
    input_id = input("Введи id клиента для удаления ")
    cur.execute("""
    SELECT client_name, client_surname FROM client_data WHERE client_id=%s
    """, (input_id))
    client_delete = cur.fetchone()
    confirm = input(f"Удалить {client_delete} - да/нет")
    if confirm == "да" or confirm == "д":
        cur.execute("""
        DELETE FROM numbers_phone WHERE client_phone_id=%s
        """, (input_id))

        cur.execute("""
        DELETE FROM client_data WHERE client_id=%s
        """, (input_id))
    else:
        return delete_client_data(cur)

def search_client(cur):
    print("найти по имени - 1\nнайти по фамилии - 2\nнайти по email - 3"
          "\nнайти по номеру телефона - 4\nвыйти - 0")
    while True:
        input_command = int(input("_ "))
        if input_command not in [1, 2, 3, 4, 0]:
            print("нет такой команды")
            return search_client(cur)
        elif input_command == 0:
            break
        else:
            if input_command == 1:
                input_name = input("Введи имя клиента ")
                print(input_name)
                cur.execute("""
                SELECT client_id, client_data.client_name, client_data.client_surname,
                client_data.client_email, numbers_phone.client_number_phone
                FROM client_data 
                LEFT JOIN numbers_phone ON numbers_phone.client_phone_id = client_data.client_id
                WHERE client_data.client_name = '{}';
                """.format(input_name)) # вот только так и заработало, хотя на лекции сказали,
                print(cur.fetchall())  # хотя на лекции сказали, что так плохо, а name=%s выдает ошибку

            if input_command == 2:
                input_surname = input("Введи фамилию клиента ")
                cur.execute("""
                SELECT client_id, client_data.client_name, client_data.client_surname,
                client_data.client_email, numbers_phone.client_number_phone
                FROM client_data 
                LEFT JOIN numbers_phone ON numbers_phone.client_phone_id = client_data.client_id
                WHERE client_data.client_surname = '{}';
                """.format(input_surname))
                print(cur.fetchall())

            if input_command == 3:
                input_email = input("Введи эл. адресс клиента ")
                cur.execute("""
                SELECT client_id, client_data.client_name, client_data.client_surname,
                client_data.client_email, numbers_phone.client_number_phone
                FROM client_data 
                LEFT JOIN numbers_phone ON numbers_phone.client_phone_id = client_data.client_id
                WHERE client_data.client_email = '{}';
                """.format(input_email))
                print(cur.fetchall())

            if input_command == 4:
                input_number_phone = input("Введи номер телефона клиента ")
                cur.execute("""
                SELECT client_id, client_data.client_name, client_data.client_surname,
                client_data.client_email, numbers_phone.client_number_phone
                FROM client_data 
                LEFT JOIN numbers_phone ON numbers_phone.client_phone_id = client_data.client_id
                WHERE numbers_phone.client_number_phone = '{}';
                """.format(input_number_phone))
                print(cur.fetchall())

# отображения таблиц
def examination(cur):
    cur.execute("""
        SELECT * FROM client_data;
    """)
    pprint(cur.fetchall())

    cur.execute("""
        SELECT * FROM numbers_phone;
    """)
    pprint(cur.fetchall())

conn = psycopg2.connect(database='homework_5', user='postgres', password='0302103')
with conn.cursor() as cur:

    # удалим ранее созданные таблицы, для исключения ошибок
    cur.execute("""
        DROP TABLE numbers_phone;
        DROP TABLE client_data;
    """)

    client_data(cur)
    add_data_client(cur, "Ivan", "Chankin", "xnvn@mail.ru")
    add_data_client(cur, "Petro", "Kuruev", "fjhds@inbox.ru")
    add_data_client(cur, "Cemen", "Zaralin", "adjjv@mail.ru")
    add_data_client(cur, "Aderim", "Delimov", "sjfkns@.com")
    add_number_phone(cur, 1, "89059999999")
    add_number_phone(cur, 1, "89057777777")
    add_number_phone(cur, 2, "89054449999")
    add_number_phone(cur, 2, "89104442222")
    add_number_phone(cur, 3, "89055555555")
    add_number_phone(cur, 3, "89055678965")
    add_number_phone(cur, 4, "89024252567")
    examination(cur)
    change_data_client()
    #delete_phone_client(cur)
    #delete_client_data(cur)
    #search_client(cur)
    examination(cur)

conn.commit()
conn.close()