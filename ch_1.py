import sqlite3

conn = sqlite3.connect('static/botDB.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_completion(user_id: str, about: str):
    cursor.execute('SELECT * FROM alb WHERE user_id = ?', (user_id,))
    info = cursor.fetchone()
    if info is None:
        cursor.execute('INSERT INTO alb (user_id, about) VALUES (?, ?)', (user_id, about))
        conn.commit()
    else:
        cursor.execute("""UPDATE alb SET about = ? WHERE id = ?""", (about, info[0]))
        conn.commit()


def set_like(user_id: str):
    cursor.execute('SELECT * FROM alb WHERE user_id = ?', (user_id,))
    info = cursor.fetchone()
    if info is None:
        print(f'нет такого пользователя: {user_id}')
        return False
    else:
        cursor.execute("""UPDATE alb SET like = ? WHERE id = ?""", (info[3] + 1, info[0]))
        print(f'успешно добавлен лайк для пользователя {user_id}')
        conn.commit()
        return True


def set_dislike(user_id: str):
    cursor.execute('SELECT * FROM alb WHERE user_id = ?', (user_id,))
    info = cursor.fetchone()
    if info is None:
        print(f'нет такого пользователя: {user_id}')
        return False
    else:
        cursor.execute("""UPDATE alb SET dislike = ? WHERE id = ?""", (info[4] + 1, info[0]))
        print(f'успешно добавлен дизляйк для пользователя {user_id}')
        conn.commit()
        return True


def get_like(user_id: str):
    cursor.execute('SELECT * FROM alb WHERE user_id = ?', (user_id,))
    info = cursor.fetchone()
    if info is None:
        print(f'нет такого пользователя: {user_id}')
        return None
    else:
        return info[3]


def get_dislike(user_id: str):
    cursor.execute('SELECT * FROM alb WHERE user_id = ?', (user_id,))
    info = cursor.fetchone()
    if info is None:
        print(f'нет такого пользователя: {user_id}')
        return None
    else:
        return info[4]


def get_about(user_id: str):
    cursor.execute('SELECT * FROM alb WHERE user_id = ?', (user_id,))
    info = cursor.fetchone()
    if info is None:
        print(f'нет такого пользователя: {user_id}')
        return None
    else:
        return info[2]

