from datetime import datetime

from peewee import OperationalError

from db.model import db, User, Action


def backup_table_and_drop(table_obj):
    try:
        if table_obj.select().count() > 0:
            db.execute_sql(
                f"create table {table_obj.__name__.lower()}_{s} " f"as select * from {table_obj.__name__.lower()}"
            )
            print(f"Backup created {table_obj.__name__.lower()}")
        db.drop_tables([table_obj])
    except OperationalError:
        print(f"Backup error {table_obj.__name__.lower()}")


def insert_data_from_backup(table_obj):
    try:
        db.execute_sql(f"insert into {table_obj.__name__.lower()}" f" select * from {table_obj.__name__.lower()}_{s}")
        print(f"{table_obj.__name__.lower()} - restored")
    except OperationalError as e:
        print(f"Recovery error {table_obj.__name__.lower()}", {e})


if "__main__" == __name__:
    print("Press Enter to run process.")
    input()

    s = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    tbls = [
        User,
        Action,
    ]
    for t in reversed(tbls):
        backup_table_and_drop(t)

    db.create_tables(tbls)

    for tb in [User, Action]:
        insert_data_from_backup(tb)
