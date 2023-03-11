"""Tests for the `UsersDBMySql`."""


import pytest

from past_years.auth_utils import hash_password, valid_password
from past_years.db import UsersDBMySql
from past_years.errors import UserNotFoundError, UserWithEmailExistsError
from tests.utils import MockUser, get_user

# ----- Constants -----
PASSWORD = "password"

# ----- Tests ----


def test_get_user(user_db: UsersDBMySql, existing_user: MockUser):

    user = user_db.get_user(existing_user.user_id)

    assert user.user_id == existing_user.user_id
    assert user.display_name == existing_user.display_name
    assert user.email == existing_user.email


def test_get_password(user_db: UsersDBMySql, existing_user: MockUser):

    pwd = user_db.get_user_password(existing_user.user_id)

    assert valid_password(existing_user.password, pwd) is True


def test_get_password_invalid_user_id(user_db: UsersDBMySql):

    with pytest.raises(UserNotFoundError):
        user_db.get_user_password("invalid")


def test_get_user_invalid_user_id(user_db: UsersDBMySql):

    with pytest.raises(UserNotFoundError):
        user_db.get_user("invalid")


def test_add_user(user_db: UsersDBMySql):

    user = get_user()
    pwd = hash_password(PASSWORD)
    new_user = user_db.add_user(user, pwd)

    assert new_user.user_id

    new_user = user_db.get_user(new_user.user_id)

    assert new_user.display_name == user.display_name
    assert new_user.email == user.email


def test_add_user_with_same_email(user_db: UsersDBMySql):

    user = get_user()
    pwd = hash_password(PASSWORD)

    user_db.add_user(user, pwd)
    user.user_id = ""

    with pytest.raises(UserWithEmailExistsError):
        user.display_name = "Another name"
        user_db.add_user(user, pwd)


def test_edit_user(user_db: UsersDBMySql):

    user_id = "1"
    # previous user details
    # display_name = Shruti
    # email - shruti@gmail.com
    user = get_user()
    user.user_id = user_id

    user_db.edit_user(user)
    edited_user = user_db.get_user(user_id)

    assert edited_user.display_name == user.display_name
    assert edited_user.email == user.email


def test_delete_user(user_db: UsersDBMySql):

    user = get_user()
    pwd = hash_password(PASSWORD)
    user = user_db.add_user(user, pwd)

    user_db.delete_user(user.user_id)

    with pytest.raises(UserNotFoundError):
        user_db.get_user(user.user_id)
