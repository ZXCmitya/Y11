def set_session_token(token: str):
    with open("session_token", "w") as token_file:
        token_file.write(token)


def get_session_token() -> str:
    with open("session_token", "r") as token_file:
        return token_file.read()


def set_current_style(theme: str):
    with open(f"current_style.txt", "w") as style_file:
        style_file.write(theme)


def get_style_name():
    with open(f"current_style.txt", "r") as style_file:
        return style_file.read()


def get_current_style_css(theme: str):
    with open(f"styles/{theme}.txt", "r") as style_file:
        return style_file.read()


def save_note(text: str):
    with open(f"note.txt", "w") as note_file:
        return note_file.write(text)


def get_note() -> str:
    with open(f"note.txt", "r") as note_file:
        return note_file.read()
