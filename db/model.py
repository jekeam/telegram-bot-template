from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    BigIntegerField,
    Model,
    SqliteDatabase,
    PrimaryKeyField,
)

db = SqliteDatabase(database="database.sqlite", timeout=10, check_same_thread=False)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = BigIntegerField(unique=True, primary_key=True)
    role = CharField(null=False, default="client")
    status = CharField(null=False, default="on")
    name_first = CharField(null=True)
    name_last = CharField(null=True)
    username = CharField(null=True)
    url = CharField(null=True)
    phone = CharField(null=True)
    geo = CharField(null=True)
    language_code = CharField(null=True)
    email = CharField(null=True)
    last_touch = DateTimeField(null=True)


class Action(BaseModel):
    id = PrimaryKeyField(unique=True)
    user_id = BigIntegerField(null=False)
    action_time = DateTimeField(null=True, default=datetime.now)
    message_id = BigIntegerField(null=True)
    parent_message_id = BigIntegerField(null=True)
    message = CharField(null=False, max_length=4096)
