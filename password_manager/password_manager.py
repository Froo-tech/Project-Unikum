import sqlite3
import hashlib

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
    else:
        print("Пользователь с таким username уже существует!")
else:



    pash = hashlib.sha256(pas.encode()).hexdigest()

    c.execute('INSERT INTO Users (username, email, age, pas) VALUES (?, ?, ?, ?)', (us, email, age, pash))


    c.commit()
c.close()
