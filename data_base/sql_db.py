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


async def read_auth(id_user):
    return cur.execute('SELECT phone, password FROM user_auth WHERE id_user == ?', (id_user,)).fetchone()


async def read_admin(id_user):
    return cur.execute('SELECT id_admin FROM admins WHERE id_admin == ?', (id_user,)).fetchone()


async def read_all_admins():
    return cur.execute('SELECT * FROM admins').fetchall()


async def read_all_salon():
    return cur.execute('SELECT * FROM salons').fetchall()


async def creat_auth_user(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO user_auth VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


async def creat_admin(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO admins VALUES (?, ?)', tuple(data.values()))
        base.commit()


async def creat_salon(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO salons VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def delete_auth(user_id):
    cur.execute('DELETE FROM user_auth WHERE id_user==?', (user_id,))
    base.commit()


async def delete_admin(user_id):
    cur.execute('DELETE FROM admins WHERE id_admin==?', (user_id,))
    base.commit()


async def delete_salon_s(user_id):
    cur.execute('DELETE FROM salons WHERE id_vk==?', (user_id,))
    base.commit()
