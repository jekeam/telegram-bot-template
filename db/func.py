from datetime import datetime

from peewee import ModelSelect

from config import ADMINS
from db.model import User, Action


def set_user(user_id, first, last, username, url, lang_code) -> None:
    try:
        User.select().where(User.id == user_id).get()
        User.update(
            name_first=first,
            name_last=last,
            username=username,
            url=url,
            last_touch=datetime.now(),
            status="on",
            role="admin" if user_id in ADMINS else "user",
            language_code=lang_code,
        ).where(User.id == user_id).execute()
    except User.DoesNotExist:
        User.insert(
            {
                User.id: user_id,
                User.name_first: first,
                User.name_last: last,
                User.username: username,
                User.url: url,
                User.last_touch: datetime.now(),
                User.status: "on",
                User.role: "admin" if user_id in ADMINS else "user",
                User.language_code: lang_code,
            }
        ).execute()


def set_user_status(user_id: int, status: str) -> None:
    User.update(
        status=status,
    ).where(User.id == user_id).execute()


def set_user_action(user_id: int, message: str, message_id: int = None, parent_message_id: int = None) -> None:
    Action.insert(
        {
            Action.user_id: user_id,
            Action.message: message,
            Action.message_id: message_id,
            Action.parent_message_id: parent_message_id,
        }
    ).execute()


def set_parrent_message_id(message_id: int, parent_message_id: int) -> None:
    Action.update(parent_message_id=parent_message_id - 1).where(Action.message_id == message_id).execute()


def get_user(user_id: int) -> ModelSelect:
    return User.select().where(User.id == user_id)


def set_last_touch(user_id) -> None:
    User.update(last_touch=datetime.now()).where(User.id == user_id).execute()


def get_admins() -> ModelSelect:
    return User.select().where(User.role == "admin")
