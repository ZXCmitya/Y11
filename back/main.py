from datetime import timedelta, datetime, timezone
from typing import Optional, List
import time
import uvicorn
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

from pydantic import BaseModel
from schemas import User, UserAuth
import db

print(datetime.utcnow())
print(datetime.now().astimezone().tzinfo)
print(datetime.now().astimezone())

app = FastAPI()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(userauth: UserAuth) -> User | bool:
    userdb = db.get_user_by_username(userauth.username)
    if not userdb:
        return False
    if not verify_password(userauth.password, userdb.password):
        return False
    return userdb


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.get_user_by_username(token_data.username)

    if user is None:
        raise credentials_exception
    return user


def token_is_working(token: str = Depends(oauth2_scheme)) -> bool:
    isValid = True

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        isValid = False

    return isValid


def datetime_to_str(datetime_object: datetime) -> str:
    datetime_str = datetime.strftime(datetime_object, '%d.%m.%y %H:%M:%S')
    return datetime_str


def add_offset(datetime_str: str) -> str:  # 24.05.24 13:16:09 - example input and output
    tz = -time.timezone
    # print(f'Часы: {tz // 3600}, Минуты: {int(tz / 3600 % 1 * 60)}')
    tz_hours = tz // 3600
    tz_minutes = int(tz / 3600 % 1 * 60)
    datetime_object = (datetime.strptime(datetime_str, '%d.%m.%y %H:%M:%S')
                       + timedelta(hours=tz_hours, minutes=tz_minutes))  # формат datetime для добавления offset'а
    res = datetime_to_str(datetime_object)  # перевод в строчный формат с offset
    return res


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = authenticate_user(UserAuth(username=form_data.username, password=form_data.password))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


# @app.post("/logout")
# def user_logout(authorization: str = Header(None)):
#     oauth2_scheme.revoke_token(authorization)
#     return {"message": "Token revoked"}

@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/users")
def get_user() -> List[User]:
    return db.get_all_users()


@app.get("/user")
def get_user_by_id(id: int) -> User:
    return db.get_user_by_id(id)


@app.post("/registration")
def register(user: User):
    user.password = get_password_hash(user.password)

    if db.add_user(user):
        return JSONResponse(status_code=status.HTTP_200_OK, content="Регистрация успешна")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Что-то пошло не так")


@app.post("/create_user")
def create_user(user: User) -> int:
    if db.add_user(user):
        return 200
    return 400


@app.put("/change_user/{id}")
def change_user(id: int, user: User) -> int:
    if db.change_user(id, user):
        return 200
    return 400


@app.patch("/change_password/{id}")
def change_password(id: int, userPass: UserAuth):
    if db.change_user_password(id, userPass.password):
        return 200
    return 400


@app.delete("/delete_user/{id}")
def delete_user(id: int, current_user: User = Depends(get_current_user)):
    if db.delete_user(id):
        return JSONResponse(status_code=status.HTTP_200_OK, content="Пользователь удалён успешно")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Произошла ошибка")


# Общий вид запроса
# https://google.com/{path}/{path}?{query}={value}&{query}={value}

# "http://127.0.0.1:8000/hello"
# Ответ: "Hello, world!"

# Запуск веб-сервера
# uvicorn main:app --reload


if __name__ == '__main__':
    uvicorn.run("main:app")
