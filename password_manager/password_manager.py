import sqlite3
import hashlib


def reg():
    c = sqlite3.connect("ps1.db")
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

    while "@" not in email:
        email = input("Введите корректный e-mail: ")

    age = int(input("age: "))
    pas = input("pas: ")

    cr.execute('SELECT * FROM Users WHERE username = ? OR email = ?', (us, email))
    existing_user = cr.fetchone()

    if existing_user:
        if existing_user[2] == email:
            print("Пользователь с таким email уже существует!")
            Status_reg = "replay_email"
        else:
            print("Пользователь с таким username уже существует!")
            Status_reg = "replay_username"
    else:
        pash = hashlib.sha256(pas.encode()).hexdigest()
        c.execute('INSERT INTO Users (username, email, age, pas) VALUES (?, ?, ?, ?)', (us, email, age, pash))
        c.commit()
        Status_reg = "success"

    c.close()
    return Status_reg, us ,pas


def log(bus=None, bpas=None):
    c = sqlite3.connect("ps1.db")
    cr = c.cursor()
    if bus is not None:
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
    return Status_log, username_to_check


def exe(us):
    c = sqlite3.connect("ps1.db")
    cr = c.cursor()
    cr.execute('SELECT * FROM Users WHERE username=?', (us,))
    user_data = cr.fetchone()
    c.close()
    if user_data != None:
        return user_data

