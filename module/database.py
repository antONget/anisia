import sqlite3
from aiogram.types import Message


# можно использовать memory: вместо названия файла, чтобы хранить данные в оперативной памяти
db = sqlite3.connect('users.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username TEXT,
    name TEXT,
    phone TEXT,
    inside TEXT
)""")
db.commit()


def add_id(message: Message):
    sql.execute("SELECT id FROM users WHERE id = ?", (message.chat.id,))
    if sql.fetchone() is None:
        try:
            sql.execute(f"INSERT INTO users VALUES(?,?,?,?,?)",
                        (message.chat.id,
                         message.from_user.username,
                         'name',
                         'phone',
                         'inside'))
            db.commit()
        except:
            sql.execute(f"INSERT INTO users VALUES(?,?,?,?,?)",
                        (message.chat.id,
                         'username',
                         'name',
                         'phone',
                         'inside'))
            db.commit()


def update_name(message: Message):
    sql.execute(f"UPDATE users SET name = ? WHERE id = ?",
                (message.text,
                 message.chat.id))
    db.commit()


def update_phone(message: Message):
    print(type(message.text))
    if message.contact is not None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    sql.execute(f"UPDATE users SET phone = ? WHERE id = ?",
                (phone,
                 message.chat.id))
    db.commit()


def update_inside(message: Message):
    sql.execute(f"UPDATE users SET inside = ? WHERE id = ?",
                (message.text.replace('\n', ' '),
                 message.chat.id))
    db.commit()


def select_row(message: Message):
    sql.execute("SELECT * FROM users WHERE id = ?", (message.chat.id,))
    return sql.fetchone()

