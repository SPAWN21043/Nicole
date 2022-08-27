import sqlite3 as sq


def sql_start():
    global base
    global cur
    base = sq.connect('nicole.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS salons(
        title TEXT,
        adress TEXT,
        phone TEXT,
        id_vk INTEGER PRIMARY KEY
        );
        """
    )
    base.commit()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_auth(
        id_user INTEGER PRIMARY KEY,
        phone INTEGER,
        password TEXT
        );
        """
    )
    base.commit()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS admins(
        id_admin INTEGER PRIMARY KEY,
        name TEXT
        );
        """
    )
    base.commit()


def read_salon():
    return cur.execute('SELECT title, id_vk FROM salons').fetchall()


async def sql_read_basket(user_id):
    return cur.execute('SELECT user_sess FROM user_session WHERE id_user == ?', (user_id,)).fetchall()
