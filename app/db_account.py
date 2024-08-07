import sqlite3


def init_db():
    try:
        base = sqlite3.connect('access_users.db')
        cursor = base.cursor()
        return base, cursor
    except Exception:
        return 'connect error'


def registered_users():
    base, cursor = init_db()
    users = cursor.execute('''SELECT * FROM users ''').fetchall()
    base.close()
    return users


def check_account(login, passw):
    for user in registered_users():
        if login == user[0] and passw == user[1]:
            return True
