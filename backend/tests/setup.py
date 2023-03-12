"""A set of functions to help with the initial data setup for testing."""

import datetime as dt
import os
from pathlib import Path
from typing import Literal

import msgspec
from mysql.connector.connection import MySQLConnection

from past_years.auth.auth_utils import hash_password
from past_years.auth.token_service import TokenServiceProtocol
from past_years.configuration import config

DATA_DIR = Path(__file__).parent / "data"

data_fp = DATA_DIR / "db/users.json"
mock_users = msgspec.json.decode(data_fp.read_bytes())

TableNames = Literal["users", "tokens"]


def setup_database():
    """Sets up the database with the required tables for testing
    and seeds it with mock data."""

    db_config = config.get_db_config()
    conn = _get_connection()
    with conn:
        with conn.cursor() as curr:
            curr.execute(f"CREATE DATABASE IF NOT EXISTS {db_config.db_name};")
            curr.execute(f"USE {db_config.db_name}")

            _create_user_table(conn)
            _create_tokens_table(conn)


def teardown_database():
    """Tears down the test database."""

    db_config = config.get_db_config()
    conn = _get_connection()
    with conn.cursor() as curr:
        curr.execute(f"DROP DATABASE {db_config.db_name};")
    conn.close()


def reset_table(table_name: TableNames):
    """Resets the table.

    Deletes all the rows in the table and reseeds it.
    """

    conn = _get_connection()
    db_config = config.get_db_config()
    with conn:
        with conn.cursor() as curr:
            curr.execute(f"USE {db_config.db_name}")
            curr.execute(f"DELETE FROM {table_name}")
            conn.commit()

            if table_name == "users":
                _seed_user_table(conn)
            elif table_name == "tokens":
                _seed_tokens_table(conn)

            conn.commit()


def _create_user_table(conn: MySQLConnection):
    """Creates and seeds the users table with mock data."""

    query = """CREATE TABLE IF NOT EXISTS users(
        user_id VARCHAR(32) PRIMARY KEY,
        display_name TINYTEXT NOT NULL,
        email VARCHAR(255) UNIQUE,
        hashed_pwd BINARY(64) NOT NULL,
        salt BINARY(16) NOT NULL
    )"""
    with conn.cursor() as curr:
        curr.execute(query)


def _seed_user_table(conn: MySQLConnection):
    """Seeds the user table with testing data.

    The seeding is only done if there are no entries in the table.
    """

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

    query = "REPLACE INTO users VALUES(%s, %s, %s, %s, %s)"
    with conn.cursor() as curr:
        curr.executemany(query, user_tuples_list)
        conn.commit()


def _create_tokens_table(conn: MySQLConnection):
    query = """
    CREATE TABLE IF NOT EXISTS tokens(
        user_id VARCHAR(32) PRIMARY KEY,
        refresh_token VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """

    with conn.cursor() as curr:
        curr.execute(query)
        conn.commit()


def _seed_tokens_table(conn: MySQLConnection):
    expiry_time = dt.datetime.now(tz=dt.UTC) + dt.timedelta(days=30)
    data = [
        (user["user_id"], TokenServiceProtocol.create_jwt(user["user_id"], expiry_time))
        for user in mock_users[:2]
    ]

    query = "INSERT INTO tokens VALUES(%s, %s)"
    with conn.cursor() as curr:
        curr.executemany(query, data)
        conn.commit()


def _get_connection():
    db_config = config.get_db_config()
    return MySQLConnection(
        host=db_config.host,
        user=os.environ.get("PAST_YEARS_DB_USERNAME"),
        password=os.environ.get("PAST_YEARS_DB_PWD"),
        autocommit=True,
    )
