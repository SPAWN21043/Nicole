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
        id INTEGER PRIMARY KEY,
        title TEXT,
        adress TEXT,
        phone TEXT,
        id_vk INTEGER
        );
        """
    )
    base.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS user_session (id INTEGER PRIMARY KEY, id_user INTEGER, user_sess TEXT)''')


def sql_read_salon():
    return cur.execute('SELECT title, id_vk FROM salons').fetchall()


async def sql_read_basket(user_id):
    return cur.execute('SELECT user_sess FROM user_session WHERE id_user == ?', (user_id,)).fetchall()
