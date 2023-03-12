from typing import Protocol, cast
from uuid import uuid1

from loguru import logger
from mysql.connector import IntegrityError

from past_years.auth.auth_utils import Password
from past_years.context import ctx
from past_years.db.db import MySqlDB
from past_years.db.schemas import User
from past_years.errors import UserNotFoundError, UserWithEmailExistsError


class UsersDBProtocol(Protocol):
    """Handles all operations related to users."""

    def get_user_with_id(self, user_id: str) -> User:
        """Returns the user with the given ID.

        Raises:
            UserNotFound: Raised if the user with the given
                id was not found.
        """
        ...

    def get_user_with_email(self, email: str) -> User:
        """Returns the user with the given email address.

        Raises:
            UserNotFound: Raised if the user with the given email
                was not found.
        """
        ...

    def get_user_password(self, user_id: str) -> Password:
        """Returns the password of the user with the given user id.

        Returns:
            The password details i.e. the hashed password and the salt
            used when hashing.

        Raises:
            UserNotFoundError: Raised if the user is not found.
        """
        ...

    def add_user(self, user: User) -> User:
        """Creates a new user with the given details.

        Returns:
            The id of the newly added user.
        """
        ...

    def edit_user(self, user: User) -> User:
        """Updates the details of the user with the given details.

        NOTE: This only updates the display name and the email.
        """
        ...

    def edit_user_password(self, usr_id: str, password: Password) -> None:
        """Updates the user's password with the given password."""
        ...

    def delete_user(self, user_id: str) -> bool:
        """Deletes the user with the given user id.

        Returns:
            A boolean indicating whether the action was successful
            or not.
        """
        ...


UserDBReturnType = tuple[str, str] | None
"""The type that is returned when getting a single user."""

PasswordDBReturnType = tuple[bytearray, bytearray]
"""The type that is returned when getting the password of a single user."""


class UsersDBMySql(UsersDBProtocol):
    def __init__(self, db: MySqlDB):
        self._db = db

    def get_user_with_id(self, user_id: str) -> User:
        logger.debug(f"Getting user `{user_id}`", request_id=ctx.request_id)

        query = "SELECT display_name, email FROM users WHERE user_id=%s"
        result = self._db.execute_and_fetch_one(query, (user_id,))
        user_details: UserDBReturnType = cast(UserDBReturnType, result)

        if not user_details:
            logger.error(f"User `{user_id}` was not found", request_id=ctx.request_id)
            raise UserNotFoundError(user_id)

        return User(
            user_id=user_id,
            display_name=user_details[0],
            email=user_details[1],
        )

    def get_user_with_email(self, email: str) -> User:
        logger.debug(f"Getting user with email", request_id=ctx.request_id)

        query = "SELECT user_id, display_name FROM users WHERE email=%s"
        result = self._db.execute_and_fetch_one(query, (email,))
        user_details: UserDBReturnType = cast(UserDBReturnType, result)

        if not user_details:
            logger.error(f"User was not found", request_id=ctx.request_id)
            raise UserNotFoundError(email)

        return User(
            user_id=user_details[0],
            display_name=user_details[1],
            email=email,
        )

    def get_user_password(self, user_id: str) -> Password:
        logger.debug(f"Getting password of user `{user_id}`", request_id=ctx.request_id)

        query = """SELECT hashed_pwd, salt FROM users WHERE user_id=%s"""
        result = self._db.execute_and_fetch_one(query, (user_id,))

        if not result:
            logger.error(f"User `{user_id}` was not found")
            raise UserNotFoundError(user_id)

        return Password(bytes(result[0]), bytes(result[1]))

    def add_user(self, user: User, password: Password) -> User:
        logger.info("Adding new user", request_id=ctx.request_id)

        # Checking if user with given email already exists
        query = """SELECT COUNT(*) FROM users WHERE email=%s"""
        result = self._db.execute_and_fetch_one(query, (user.email,))

        if result and result[0]:
            logger.error("User with email already exists")
            raise UserWithEmailExistsError()

        return self._add_user(user, password)

    def edit_user(self, user: User) -> None:
        logger.debug(f"Editing user `{user.user_id}`", request_id=ctx.request_id)

        query = """
            UPDATE users
            SET
                display_name = %s,
                email = %s
            WHERE
                user_id = %s
            """

        data = (user.display_name, user.email, user.user_id)
        self._db.execute(query, data)

    def edit_user_password(self, user_id: str, password: Password) -> None:
        logger.debug(f"Editing password of user `{user_id}`", request_id=ctx.request_id)

        query = """
            UPDATE users
            SET
                hashed_pwd = %s,
                salt = %s,
            WHERE
                user_id = %s
           """

        data = (password.hashed_password, password.salt, user_id)
        self._db.execute(query, data)

    def delete_user(self, user_id: str) -> None:
        logger.debug(f"Deleting user `{user_id}`", request_id=ctx.request_id)

        query = "DELETE FROM users WHERE user_id=%s"
        self._db.execute(query, (user_id,))

    def _add_user(self, user: User, password: Password) -> User:
        """Adds the given user to the database, but also ensures
        that the generated user ID is unique."""

        unique_id = uuid1().hex
        id_len = 6
        user_id = unique_id[:id_len]

        while True:
            logger.trace(
                f"Attempting to add user `{user_id}`", request_id=ctx.request_id
            )

            query = """INSERT INTO users VALUES(%s, %s, %s, %s, %s)"""
            data = (
                user_id[:id_len],
                user.display_name,
                user.email,
                password.hashed_password,
                password.salt,
            )
            try:
                self._db.execute(query, data)
            except IntegrityError as ex:
                # Happens when the user id is a duplicate
                logger.error(f"User not added - {str(ex)}")
                id_len += 1
                user_id = unique_id[:id_len]
                assert id_len <= 32, "User ID length exceeded 32"
                continue

            logger.debug(f"Added user `{user_id}`", request_id=ctx.request_id)

            user.user_id = user_id
            return user
