import sqlite3
from typing import Optional, List
from pyd import User


def create_table():
    connect = sqlite3.connect("data.db")

    connect.execute("""
        CREATE TABLE IF NOT EXISTS users (
            "id" INTEGER NOT NULL UNIQUE,
            "name" TEXT,
            "username" TEXT,
            "password" TEXT,
            "email" TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
    """)


def add_user(user: User) -> bool:
    connect = sqlite3.connect("data.db")

    connect.execute("""INSERT INTO users (name, username, password, email) VALUES (?, ?, ?, ?);""",
                    list(user.dict().values())[1:])
    connect.commit()

    connect.close()
    return True


def get_all_users() -> List[User]:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute("""SELECT * FROM users; """)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        res.append(
            User(**{key: value for key, value in zip(User.model_fields.keys(), row)}))
    return res


def get_user_by_username(username: str) -> User | bool:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute(
        """SELECT * FROM users WHERE "username" = ?;""",
        [username])
    row = cursor.fetchone()
    if row is None:
        return False
    return User(
        **{key: value for key, value in zip(User.model_fields.keys(), row)})


def get_user_by_id(id: int) -> User | bool:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute("""SELECT * FROM users WHERE "id" = ?;""", [id])
    row = cursor.fetchone()
    if row is None:
        return False
    return User(
        **{key: value for key, value in zip(User.model_fields.keys(), row)})


def change_user(id: int, user: User) -> bool:
    connect = sqlite3.connect("data.db")
    params = list(user.dict().values())[1:]
    params.append(id)

    connect.execute("""UPDATE users SET (name, username, password, email) = (?, ?, ?, ?) WHERE id = ?;""",
                    params)
    connect.commit()
    return True


def change_user_password(id: int, password: str) -> bool:
    connect = sqlite3.connect("data.db")
    connect.execute(
        """UPDATE users SET password = ? WHERE id = ?;""", [
            password, id])
    connect.commit()
    return True


def delete_user(id: int) -> bool:
    connect = sqlite3.connect("data.db")
    connect.execute("""DELETE FROM users WHERE id = ?;""", [id])
    connect.commit()
    return True


if __name__ == '__main__':
    create_table()
