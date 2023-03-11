"""A set of functions to help with the initial data setup for testing."""

import os
from pathlib import Path
from typing import Literal

import msgspec
from mysql.connector.connection import MySQLConnection

from past_years.auth_utils import hash_password
from past_years.configuration import config

DATA_DIR = Path(__file__).parent / "data"

TableNames = Literal["users"]


def setup_database():
    """Sets up the database with the required tables for testing
    and seeds it with mock data."""

    db_config = config.get_db_config()
    assert db_config.db_name.startswith(
        "test"
    ), "The database doesn't seem to be a test database"

    conn = _get_connection()
    with conn:
        with conn.cursor() as curr:
            curr.execute(f"CREATE DATABASE {db_config.db_name};")
            curr.execute(f"USE {db_config.db_name}")

            _create_user_table(conn)


def teardown_database():
    """Tears down the test database."""

    db_config = config.get_db_config()
    conn = _get_connection()
    with conn.cursor() as curr:
        curr.execute(f"DROP DATABASE {db_config.db_name};")
    conn.close()


def reset_table(table_name: Literal["users"]):
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
            conn.commit()


def _create_user_table(conn: MySQLConnection):
    """Creates and seeds the users table with mock data."""

    query = """CREATE TABLE users(
        user_id VARCHAR(32) PRIMARY KEY,
        display_name TINYTEXT NOT NULL,
        email VARCHAR(255) UNIQUE,
        hashed_pwd BINARY(64) NOT NULL,
        salt BINARY(16) NOT NULL
    )"""
    with conn.cursor() as curr:
        curr.execute(query)


def _seed_user_table(conn: MySQLConnection):
    """Seeds the user table with testing data."""

    data_fp = DATA_DIR / "db/users.json"
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

    query = "INSERT INTO users VALUES(%s, %s, %s, %s, %s)"
    with conn.cursor() as curr:
        print("I'M HERE")
        curr.executemany(query, user_tuples_list)
        print("EFFECTED ROWS =", curr.rowcount)
        conn.commit()


def _get_connection():
    db_config = config.get_db_config()
    return MySQLConnection(
        host=db_config.host,
        user=os.environ.get("PAST_YEARS_DB_USERNAME"),
        password=os.environ.get("PAST_YEARS_DB_PWD"),
        autocommit=True,
    )
