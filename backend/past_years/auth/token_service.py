import datetime as dt
import os
from typing import Any, Protocol

import jwt
from jwt import PyJWTError
from loguru import logger

from past_years.context import ctx
from past_years.db.db import MySqlDB
from past_years.errors import InvalidTokenError


class TokenServiceProtocol(Protocol):
    """Handles creation/verification of access tokens."""

    def create_refresh_token(self, user_id: str) -> str:
        """Returns a new refresh token."""
        ...

    def get_refresh_token(self, user_id: str) -> str:
        """Returns a refresh token for the user from the
        database, if present."""
        ...

    def delete_refresh_token(self, user_id: str):
        """Deletes the refresh token for the given user."""
        ...

    def get_access_token_from_refresh_token(self, token: str) -> bool:
        """Validates the refresh token."""
        ...

    @staticmethod
    def create_jwt(user_id: str, expiry_time: dt.datetime | None = None) -> str:
        """Returns a new access token."""

        if not expiry_time:
            expiry_time = dt.datetime.now(tz=dt.UTC) + dt.timedelta(minutes=15)
        payload = {"user_id": user_id, "exp": expiry_time, "iss": "PastQuest"}

        key = os.environ["PAST_YEARS_JWT_KEY"]
        return jwt.encode(payload, key)

    @staticmethod
    def validate_access_token(token: str) -> dict[str, Any]:
        """Validates the given access token."""

        key = os.environ["PAST_YEARS_JWT_KEY"]
        try:
            return jwt.decode(token, key, algorithms=["HS256"])
        except PyJWTError as ex:
            logger.error(f"Invalid JWT - {ex}", request_id=ctx.request_id)
            raise InvalidTokenError("Invalid token") from ex


class TokenServiceMySql(TokenServiceProtocol):
    def __init__(self, db: MySqlDB):
        self._db = db

    def create_refresh_token(self, user_id: str) -> str:
        expiry_time = dt.datetime.now(tz=dt.UTC) + dt.timedelta(days=30)
        refresh_token = self.create_jwt(user_id, expiry_time)

        query = "REPLACE INTO tokens (user_id, refresh_token) VALUES(%s, %s)"
        self._db.execute(query, (user_id, refresh_token))

        return refresh_token

    def get_refresh_token(self, user_id: str) -> str:
        query = "SELECT refresh_token FROM tokens WHERE user_id=%s"

        result = self._db.execute_and_fetch_one(query, (user_id,))

        if not result:
            return ""
        return result[0]

    def delete_refresh_token(self, user_id: str):
        query = "DELETE FROM tokens WHERE user_id=%s"
        self._db.execute(query, (user_id,))

    def get_access_token_from_refresh_token(self, token: str) -> str:
        payload = self.validate_access_token(token)

        user_id = payload["user_id"]
        refresh_token = self.get_refresh_token(user_id)
        if refresh_token != token:
            logger.error("Refresh tokens don't match", request_id=ctx.request_id)
            raise InvalidTokenError("Refresh tokens don't match")

        return self.create_jwt(user_id)
