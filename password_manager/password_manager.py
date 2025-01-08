import sqlite3
import hashlib


def reg():
    c = sqlite3.connect("ps1.bd")
    cr = c.cursor()


    cr.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    email TEXT,
                    age INTEGER,
                    pas TEXT
                )''')


    us = input("username: ")
    email = input("email: ")

    emaill = list(email)
    while "@" not in emaill:
        emaill = input("Введите корректный e-mail: ")
        email = emaill

    age = int(input("age: "))
    pas = input("pas: ")
    cr.execute('SELECT * FROM Users WHERE username = ? OR email = ?', (us, email))
    existing_user = cr.fetchone()

    if existing_user:
        if email in existing_user:
            print("Пользователь с таким email уже существует!")
            Status_reg = "replay_email"
        else:
            print("Пользователь с таким username уже существует!")
            Status_reg = "replay_username"
    else:



        pash = hashlib.sha256(pas.encode()).hexdigest()

        c.execute('INSERT INTO Users (username, email, age, pas) VALUES (?, ?, ?, ?)', (us, email, age, pash))


        c.commit()

    c.close()
    return Status_reg

def log(bus = None, bpas = None):
    c = sqlite3.connect("ps1.bd")
    cr = c.cursor()
    if bus != None :
        username_to_check = bus
        password_to_check = bpas
    else:
        username_to_check = input("Введите имя пользователя: ")
        password_to_check = input("Введите пароль: ")

    cr.execute('SELECT pas FROM Users WHERE username = ?', (username_to_check,))
    result = cr.fetchone()

    if result:
        stored = result[0]

        input_password = hashlib.sha256(password_to_check.encode()).hexdigest()

        if input_password == stored:
            print("Доступ получен!")
            Status_log = True
        else:
            print("Запрет входа!")
            Status_log = False
    else:
        print("Пользователь не найден.")
        Status_log = False

    c.close()
    return Status_log
