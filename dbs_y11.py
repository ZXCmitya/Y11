import sqlite3
from typing import Optional, List
from pyd import User


def create_table_with_users():
    connect = sqlite3.connect("data.db")

    connect.execute("""
        CREATE TABLE IF NOT EXISTS "Users" (
            "id" INTEGER NOT NULL UNIQUE,
            "name" TEXT,
            "username" TEXT,
            "password" TEXT,
            "email" TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
    """)

#====================================================================================================
# def add_user(user: User) -> bool:
#     connect = sqlite3.connect("data.db")

#     connect.execute("""INSERT INTO "Users" (name, username, password, email) VALUES (?, ?, ?, ?);""",
#                     list(user.dict().values())[1:])
#     connect.commit()

#     connect.close()
#     return True
#====================================================================================================

def get_user_by_username(username: str) -> User | bool:
    conn = sqlite3.connect("data.db")
    cursor = conn.execute("""SELECT * FROM "Users" WHERE "username" = ?;""", [username])
    row = cursor.fetchone()
    if row is None:
        return False
    return User(**{key: value for key, value in zip(User.model_fields.keys(), row)})