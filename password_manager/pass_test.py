import sqlite3
import hashlib


c = sqlite3.connect("ps1.bd")
cr = c.cursor()


username_to_check = input("Введите имя пользователя: ")
password_to_check = input("Введите пароль: ")


cr.execute('SELECT pas FROM Users WHERE username = ?', (username_to_check,))
result = cr.fetchone()


if result:
    stored = result[0]

    input_password = hashlib.sha256(password_to_check.encode()).hexdigest()

    if input_password == stored:
        print("Доступ получен!")
    else:
        print("Запрет входа!")
else:
    print("Пользователь не найден.")


c.close()
