import sqlite3
import hashlib
import logging
import re
import bcrypt
logging.basicConfig(level=logging.INFO)

class Password:

    _instance = None
    
    def __init__(self):
        self.db_name = "ps1.db"
        
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Password, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def reg(self, bus=None, bpas=None):
        logs = ""
        with sqlite3.connect(self.db_name) as conn:
            cr = conn.cursor()

            cr.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            email TEXT UNIQUE,
                            age INTEGER CHECK(age > 0),
                            pas TEXT
                        )''')
            logs += "init_db\n"
            logging.info("Database initialized")

            if bus is None:
                us = input("username: ")
            else:
                us = bus

            while True:
                email = input("email: ")
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    break
                logging.warning(f"Invalid email: {email}")
                print("Введите корректный e-mail: ")

            while True:
                try:
                    age = int(input("age: "))
                    if age <= 0:
                        print("Возраст должен быть положительным числом. Попробуйте снова.")
                        logging.info("Incorrect age.")
                        continue
                    break
                except ValueError:
                    print("Пожалуйста, введите корректное число.")
                    logging.warning("Incorrect age.")

            if bpas is None:
                pas = input("pas: ")
            else:
                pas = bpas

            cr.execute('SELECT * FROM Users WHERE username = ? OR email = ?', (us, email))
            existing_user = cr.fetchone()

            if existing_user:
                if existing_user[2] == email:
                    print("Пользователь с таким email уже существует!")
                    status_reg = "replay_email"
                    logging.warning(f"Replay email: {email}")
                else:
                    print("Пользователь с таким username уже существует!")
                    status_reg = "replay_username"
                    logging.warning(f"Replay username: {us}")
            else:
                pash = bcrypt.hashpw(pas.encode(), bcrypt.gensalt())
                cr.execute('INSERT INTO Users (username, email, age, pas) VALUES (?, ?, ?, ?)', (us, email, age, pash))
                conn.commit()
                status_reg = "success"
                logging.info(f"Registration successful: {us}")

        return {"status": status_reg, "username": us, "password": pas, "logs": logs}

    def log(self, bus=None, bpas=None):
        with sqlite3.connect(self.db_name) as conn:
            cr = conn.cursor()

            if bus is not None:
                username_to_check = bus
                password_to_check = bpas
            else:
                username_to_check = input("Введите имя пользователя: ")
                password_to_check = input("Введите пароль: ")

            cr.execute('SELECT pas FROM Users WHERE username = ?', (username_to_check,))
            result = cr.fetchone()

            if result:
                stored_password = result[0]
                if bcrypt.checkpw(password_to_check.encode(), stored_password):
                    print("Доступ получен!")
                    status_log = True
                    logging.info(f"Успешный вход для пользователя: {username_to_check}")
                else:
                    print("Запрет входа!")
                    status_log = False
                    logging.warning(f"failed_login_user: {username_to_check}")
            else:
                print("Пользователь не найден.")
                status_log = False
                logging.warning(f"user_not_in_db: {username_to_check}")

        return {"status": status_log, "username": username_to_check}

    def exe(self, us):
        with sqlite3.connect(self.db_name) as conn:
            cr = conn.cursor()
            cr.execute('SELECT * FROM Users WHERE username=?', (us,))
            user_data = cr.fetchone()

            if user_data is None:
                logging.warning(f"None_data {us}.")
            else:
                logging.info(f"exe_data {us}.")

        return user_data

    def adm_pas(self):
        with sqlite3.connect(self.db_name) as conn:
            cr = conn.cursor()
            cr.execute('SELECT * FROM Users')
            user_data = cr.fetchall()
            logging.info("all_extracted_been_data")

        return user_data
