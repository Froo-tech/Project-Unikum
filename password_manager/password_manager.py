import sqlite3
import hashlib
import logging


logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def reg():
    logs = ""
    c = sqlite3.connect("ps1.db")
    cr = c.cursor()

    cr.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    email TEXT UNIQUE,
                    age INTEGER CHECK(age > 0),
                    pas TEXT
                )''')
    logs += "init_db\n"
    logging.info("db_init")

    us = input("username: ")
    email = input("email: ")

    while "@" not in email:
        email = input("Введите корректный e-mail: ")
        logging.warning(f"Некорректный email: {email}")

    while True:
        try:
            age = int(input("age: "))
            if age <= 0:
                print("Возраст должен быть положительным числом. Попробуйте снова.")
                logging.info("incorrect age.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите корректное число.")
            logging.warning("incorrect age.")

    pas = input("pas: ")

    cr.execute('SELECT * FROM Users WHERE username = ? OR email = ?', (us, email))
    existing_user = cr.fetchone()

    if existing_user:
        if existing_user[2] == email:
            print("Пользователь с таким email уже существует!")
            Status_reg = "replay_email"
            logging.warning(f"replay_email: {email}")
        else:
            print("Пользователь с таким username уже существует!")
            Status_reg = "replay_username"
            logging.warning(f"replay_username: {us}")
    else:
        pash = hashlib.sha256(pas.encode()).hexdigest()
        c.execute('INSERT INTO Users (username, email, age, pas) VALUES (?, ?, ?, ?)', (us, email, age, pash))
        c.commit()
        Status_reg = "success"
        logging.info(f"reg_success: {us}")

    c.close()
    return Status_reg, us, pas, logs


def log(bus=None, bpas=None):
    c = sqlite3.connect("ps1.db")
    cr = c.cursor()

    if bus is not None:
        username_to_check = bus
        password_to_check = bpas
    else:
        username_to_check = input("Введите имя пользователя: ")
        password_to_check = input("Введите пароль: ")

    if password_to_check == "admin" and username_to_check == "admin":
        adm_pas()
        Status_log = "admin"
        logging.info("admin_mode.")
    else:
        cr.execute('SELECT pas FROM Users WHERE username = ?', (username_to_check,))
        result = cr.fetchone()

        if result:
            stored = result[0]
            input_password = hashlib.sha256(password_to_check.encode()).hexdigest()

            if input_password == stored:
                print("Доступ получен!")
                Status_log = True
                logging.info(f"Успешный вход для пользователя: {username_to_check}")
            else:
                print("Запрет входа!")
                Status_log = False
                logging.warning(f"failed_login_user: {username_to_check}")
        else:
            print("Пользователь не найден.")
            Status_log = False
            logging.warning(f"user_not_in_db: {username_to_check}")

    c.close()
    return Status_log, username_to_check


def exe(us):
    c = sqlite3.connect("ps1.db")
    cr = c.cursor()
    cr.execute('SELECT * FROM Users WHERE username=?', (us,))
    user_data = cr.fetchone()
    c.close()

    if user_data is None:

        logging.warning(f"None_data{us}.")
    else:
        logging.info(f"exe_data {us}.")

    return user_data

def adm_pas():
    c = sqlite3.connect("ps1.db")
    cr = c.cursor()
    cr.execute('SELECT * FROM Users')
    user_data = cr.fetchall()
    logging.info("all_extracted_been_data")
    c.close()

    return user_data
