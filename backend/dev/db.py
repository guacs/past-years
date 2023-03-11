from pathlib import Path

import msgspec

from past_years.auth_utils import hash_password
from past_years.configuration import config
from past_years.db.db import MySqlDB

_db: MySqlDB | None = None


def create_user_table():
    """Creates and seeds the users table with mock data."""

    query = """CREATE TABLE users(
        user_id VARCHAR(32) PRIMARY KEY,
        display_name TINYTEXT NOT NULL,
        email VARCHAR(255) UNIQUE,
        hashed_pwd BINARY(64) NOT NULL,
        salt BINARY(16) NOT NULL
    )"""

    _get_db().execute(query)
    data_fp = Path(__file__).parent / "mock_data" / "user.json"
    mock_users = msgspec.json.decode(data_fp.read_bytes())

    user_tuples_list = []
    for user in mock_users:

        pwd = hash_password(user["password"])
        user_tup = (
            user["user_id"],
            user["display_name"],
            user["email"],
            pwd.hashed_password,
            pwd.salt,
        )
        user_tuples_list.append(user_tup)

    db = _get_db()
    query = "INSERT INTO users VALUES(%s, %s, %s, %s, %s)"
    db.execute_many(query, user_tuples_list)
    db.close()


def reset_user_table():
    """Deletes the existing users table and creates a new one."""

    delete_table("users")
    create_user_table()


def delete_table(table_name: str):
    """Deletes the table with the given name."""

    db = _get_db()
    db.execute(f"DROP table {table_name}")


def _get_db() -> MySqlDB:
    """Returns a MySqlDB instance."""

    if _db:
        return _db

    db_config = config.get_db_config()
    return MySqlDB(db_config.db_name, db_config.host)
