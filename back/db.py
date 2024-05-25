from datetime import datetime
import sqlite3
from typing import List
from schemas import User, UserPosts


# uvicorn main:app --reload

def create_table():
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


def create_posts_table():
    connect = sqlite3.connect("data.db")

    connect.execute("""
        CREATE TABLE IF NOT EXISTS "Posts" (
            "id" INTEGER NOT NULL UNIQUE,
            "username" TEXT,
            "content" TEXT,
            "time_of_upload" TEXT,
            "id_of_user" INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
    """)


def add_user(user: User) -> bool:
    connect = sqlite3.connect("data.db")

    connect.execute("""INSERT INTO "Users" (name, username, password, email) VALUES (?, ?, ?, ?);""",
                    list(user.dict().values())[1:])
    connect.commit()

    connect.close()
    return True


def get_all_users() -> List[User]:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute("""SELECT * FROM "Users"; """)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        res.append(
            User(**{key: value for key, value in zip(User.model_fields.keys(), row)}))
    return res


def get_all_posts() -> List[UserPosts]:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute("""SELECT * FROM "Posts"; """)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        res.append(UserPosts(
            **{key: value for key, value in zip(UserPosts.model_fields.keys(), row)}))
    return res


def get_user_by_username(username: str) -> User | bool:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute(
        """SELECT * FROM "Users" WHERE "username" = ?;""", [username])
    row = cursor.fetchone()
    if row is None:
        return False
    return User(**{key: value for key, value in zip(User.model_fields.keys(), row)})


def get_post_table_by_username(username: str) -> UserPosts | bool:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute(
        """SELECT * FROM "Posts" WHERE "username" = ?;""", [username])
    row = cursor.fetchone()
    if row is None:
        return False
    return UserPosts(**{key: value for key, value in zip(UserPosts.model_fields.keys(), row)})


def get_posts_by_username(username: str) -> str | bool:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute(
        """SELECT posts FROM "Posts" WHERE "username" = ?;""", [username])
    posts = cursor.fetchone()
    if posts is None:
        return False
    return posts


def get_user_by_id(id: int) -> User | bool:
    connect = sqlite3.connect("data.db")

    cursor = connect.execute("""SELECT * FROM "Users" WHERE "id" = ?;""", [id])
    row = cursor.fetchone()
    if row is None:
        return False
    return User(**{key: value for key, value in zip(User.model_fields.keys(), row)})


def change_user(id: int, user: User) -> bool:
    connect = sqlite3.connect("data.db")
    params = list(user.dict().values())[1:]
    params.append(id)

    connect.execute("""UPDATE "Users" SET (name, username, password, email) = (?, ?, ?, ?) WHERE id = ?;""",
                    params)
    connect.commit()
    connect.close()
    return True


def change_user_password(id: int, password: str) -> bool:
    connect = sqlite3.connect("data.db")
    connect.execute(
        """UPDATE "Users" SET password = ? WHERE id = ?;""", [password, id])
    connect.commit()
    connect.close()
    return True


def delete_user(id: int) -> bool:
    connect = sqlite3.connect("data.db")
    connect.execute("""DELETE FROM "Users" WHERE id = ?;""", [id])
    connect.commit()
    connect.close()
    return True


def add_post(post: str, user: User) -> bool:
    connect = sqlite3.connect("data.db")
    cursor_time = datetime.now()

    connect.execute("""INSERT INTO "Posts" (username, content, time_of_upload, id_of_user) VALUES (?, ?, ?, ?);""", [
                    user.username, post, cursor_time.strftime("%Y-%m-%d %H:%M"), user.id])
    connect.commit()

    connect.close()
    return True


def get_all_posts():
    connect = sqlite3.connect("data.db")

    cursor = connect.execute("""SELECT * FROM "Posts"; """)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        res.append(UserPosts(
            **{key: value for key, value in zip(UserPosts.model_fields.keys(), row)}))
    return res


if __name__ == '__main__':
    create_table()
    create_posts_table()
    # add_user(User(name="Dmitry Puchkov", username="goblin", password="ffff", email="egrefe@gg.com"))
    # add_user(User(name="Aleksander Makedonsky", username="podbead", password="gdvrvba", email="fvccc@gg.com"))
    # add_user(User(name="Mikhail Romanov", username="nerurik", password="vbdrtx", email="dinasty@gg.com"))
    print(get_all_users())

    # user = get_user_by_id(3)
    # if user:
    #     print(user)
    #
    # user = User(name="Puchkov Dmitry", username="nilbog", password="sddfsdvs", email="gedgzzz@gg.com")
    # change_user(1, user)
    # print(get_all_users())
