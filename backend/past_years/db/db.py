import os
from typing import Any, Sequence

from mysql.connector.connection import MySQLConnection

_ParamsType = tuple | dict[str, Any] | None


class MySqlDB:
    """A class to interact with a MySQL database."""

    def __init__(self, db_name: str, host: str):
        self._conn: MySQLConnection | None = None
        self._db_name = db_name
        self._host = host

    def execute_and_fetch_all(self, query: str, params: _ParamsType = None):
        """Executes the given query and returns all the rows."""

        conn = self._get_connection()
        params = params or ()
        with conn.cursor(buffered=True) as curr:
            curr.execute(query, params)
            return curr.fetchall()

    def execute_and_fetch_one(self, query: str, params: _ParamsType = None):
        """Executes the query and return the first row, if present."""

        conn = self._get_connection()
        params = params or ()
        with conn.cursor() as curr:
            curr.execute(query, params)
            return curr.fetchone()

    def execute(self, query: str, params: _ParamsType = None) -> None:
        """Executes the query, but does not fetch the results."""

        conn = self._get_connection()
        params = params or ()
        with conn.cursor() as curr:
            curr.execute(query, params)

    def execute_many(self, query: str, params: Sequence[Sequence[Any]]):
        """Executes the query for `executemany`, but does not fetch the
        results."""

        conn = self._get_connection()
        with conn.cursor() as curr:
            curr.executemany(query, params)

    def close(self) -> None:
        """Closes the connection to the database."""

        if self._conn:
            self._conn.close()

    # ----- Private methods -----
    def _get_connection(self) -> MySQLConnection:
        """Creates the connection with MySQL database."""

        if not self._conn:
            self._conn = MySQLConnection(
                host=self._host,
                user=os.environ.get("PAST_YEARS_DB_USERNAME"),
                password=os.environ.get("PAST_YEARS_DB_PWD"),
                database=self._db_name,
                autocommit=True,
            )
        if not self._conn.is_connected():
            self._conn.connect()

        return self._conn
