import psycopg2

conn = psycopg2.connect(database='Clients', user='postgres', password='spbAlexx19758')
cur = conn.cursor()
cur.execute("""
DROP TABLE  Client;
DROP TABLE Phone;
""")

def create_table():
    cur.execute("""
        CREATE TABLE if not exists Client(
        CLIENT_ID SERIAL primary key,
        NAME VARCHAR(60) not null,
        SURNAME VARCHAR(60) not null,
        EMAIL VARCHAR(60) UNIQUE not null
        );   
    """)

    cur.execute("""
        CREATE TABLE if not exists Phone(
        PHONE VARCHAR(20) UNIQUE,
        CLIENT_ID INTEGER REFERENCES Client.CLIENT_ID
        );   
    """)
    conn.commit()

def add_client(name, surname, email):
    cur.execute(""" 
        INSERT INTO Client 
        (NAME, SURNAME, EMAIL) VALUES (name, surname, email);
    """)
    conn.commit()

def add_phone(phone, name):
    cur.execute(""" 
        INSERT INTO
        (SELECT Phone.PHONE FROM Phone
        JOIN Client ON Phone.CLIENT_ID=Client.CLIENT_ID
        WHERE Client.NAME=name)
        VALUES (phone);
    """)
    conn.commit()

def change_client_email(email, name):
    cur.execute(""" 
        UPDATE Client SET EMAIL (email)
        WHERE NAME=name;
    """)
    conn.commit()

def change_client_surname(surname, name):
    cur.execute(""" 
        UPDATE Client SET SURNAME (surname)
        WHERE NAME=name;
    """)
    conn.commit()

def change_client_name(name, surname):
    cur.execute(""" 
        UPDATE Client SET NAME (name)
        WHERE SURNAME=surname;
    """)
    conn.commit()

def change_phone(phone, name):
    cur.execute(""" 
        UPDATE Phone SET Phone (phone)
        WHERE Phone.CLIENT_ID=(SELECT Client.CLIENT_ID FROM Client
        JOIN Phone ON Client.CLIENT_ID=Phone.CLIENT_ID
        WHERE Client.name=name);
    """)
    conn.commit()

def delete_phone(phone):
    cur.execute(""" 
        DELETE FROM Phone 
        WHERE PHONE=phone;
    """)
    conn.commit()

def delete_client_name(name):
    cur.execute(""" 
        DELETE FROM Client 
        WHERE NAME=name;
    """)
    conn.commit()

def delete_client_surname(surname):
    cur.execute(""" 
        DELETE FROM Client 
        WHERE SURNAME=surname;
    """)
    conn.commit()

def delete_client_email(email):
    cur.execute(""" 
        DELETE FROM Client 
        WHERE EMAIL=email;
    """)
    conn.commit()

def delete_client_phone(phone):
    cur.execute(""" 
        DELETE FROM Client 
        WHERE Client.CLIENT_ID=
        (SELECT Phone.CLIENT_ID FROM Phone
        WHERE Phone.PHONE=phone);
    """)
    conn.commit()

def find_client_name(name):
    cur.execute(""" 
        SELECT Client.NAME, Client.SURNAME, Client.EMAIL, Phone.PHONE FROM Client
        JOIN Phone ON Client.CLIENT_ID=Phone.CLIENT_ID
        WHERE Client.NAME=name;
    """)
    print(cur.fetchall())

def find_client_surname(surname):
    cur.execute(""" 
        SELECT Client.NAME, Client.SURNAME, Client.EMAIL, Phone.PHONE FROM Client
        JOIN Phone ON Client.CLIENT_ID=Phone.CLIENT_ID
        WHERE Client.SURNAME=surname;
    """)
    print(cur.fetchall())

def find_client_email(email):
    cur.execute(""" 
        SELECT Client.NAME, Client.SURNAME, Client.EMAIL, Phone.PHONE FROM Client
        JOIN Phone ON Client.CLIENT_ID=Phone.CLIENT_ID
        WHERE Client.EMAIL=email;
    """)
    print(cur.fetchall())

def find_client_phone(phone):
    cur.execute(""" 
        SELECT * FROM Client
        JOIN Phone ON Client.CLIENT_ID=Phone.CLIENT_ID
        WHERE Phone.PHONE=phone;
    """)
    print(cur.fetchall())

create_table()
add_client('Алина', 'Петрова', 'vasya56@mail.ru')
add_client('Алена', 'Иванова', 'alena56@mail.ru')
add_client('Катя', 'Кудря', 'katya56@list.ru')
add_client('Света', 'Сидельникова', 'sveta56@list.ru')
add_client('Яна', 'Брусникина', 'yana90@mail.ru')
add_phone('+79096748653', 'Алина')
add_phone('+79096498653', 'Алена')
add_phone('+78996498653', 'Света')
add_phone('+78476498653', 'Яна')
add_phone('+78096498653', 'Света')
change_client_email('alina78@list.ru', 'Алина')
change_client_surname('Сидорова', 'Алина')
change_client_name('Ирина', 'Сидорова')
change_phone('89056754274', 'Ирина')
delete_phone('89056754274')
delete_client_name('Ирина')
delete_client_surname('Иванова')
delete_client_email('katya56@list.ru')
delete_client_phone('+78476498653')
find_client_name('Света')
find_client_surname('Сидельникова')
find_client_email('sveta56@list.ru')
find_client_phone('+78996498653')

cur.close()
conn.close()
