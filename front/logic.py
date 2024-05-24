def set_session_token(token: str):
    with open("session_token", "w") as token_file:
        token_file.write(token)


def get_session_token() -> str:
    with open("session_token", "r") as token_file:
        return token_file.read()

