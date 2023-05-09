from telegram import User


def more_char(_text: str, _min: int) -> bool:
    cnt = 0
    for char in _text:
        if char.isalpha():
            cnt = cnt + 1
        if cnt > _min:
            return True
    return False


def get_msg(user: User, msg: str):
    import config
    return config.LANG.get(user.language_code, config.LANG[config.DEFAULT_LANG])[msg]
