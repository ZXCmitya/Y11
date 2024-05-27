from typing import List

from front.logic import set_session_token, get_session_token
from front.schemas import User, UserAuth, UserPosts
import requests

apilink = "http://127.0.0.1:8000"


def authorize(userauth: UserAuth) -> bool:
    # print(userauth)
    # print(userauth.dict())
    res = requests.post(apilink + "/token", data=userauth.dict())

    if res.status_code != 200:
        return False

    set_session_token(res.json()["access_token"])

    return True


def get_current_user() -> User:
    header = {
        "Authorization": f"Bearer {get_session_token()}"
    }

    res = requests.get(apilink + f"/users/me", headers=header)

    return User(**res.json())


def get_current_user_json() -> dict:
    header = {
        "Authorization": f"Bearer {get_session_token()}"
    }

    res = requests.get(apilink + f"/users/me", headers=header)

    return res.json()


def get_all_users() -> List[User]:
    res = requests.get(apilink + "/users")

    return [User(**user) for user in res.json()]


def get_user_by_id(id: int) -> User:
    res = requests.get(apilink + f"/user?id={id}")

    return User(**res.json())


def register_user(user: User) -> bool:
    res = requests.post(apilink + "/registration", json=user.dict())

    return res.status_code == 200


def remove_user(id: int) -> bool:
    header = {
        "Authorization": f"Bearer {get_session_token()}"
    }

    res = requests.delete(apilink + f"/delete_user/{id}", headers=header)

    return res.status_code == 200


def create_post(post: str, user: User) -> bool:
    header = {
        "Authorization": f"Bearer {get_session_token()}"
    }
    post = {"post": post}

    res = requests.post(apilink + "/create_post", headers=header, params=post, json=user.json())

    return res.status_code == 200


def get_all_posts() -> List[UserPosts]:

    res = requests.get(apilink + "/get_all_posts")

    return [UserPosts(**post) for post in res.json()]


def change_password(user_pass: str, current_user: User) -> bool:

    header = {
        "Authorization": f"Bearer {get_session_token()}"
    }
    res = requests.patch(apilink + "/change_password/{id}?user_pass=",
                         headers=header, params=user_pass, json=current_user.dict())

    return res.status_code == 200
