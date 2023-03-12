"""Tests that don't have a natural grouping."""

from past_years.auth import hash_password, valid_password


def test_valid_password():
    """Testing with the correct password."""

    pwd = "strongest_password_ever"
    hashed_pwd = hash_password(pwd)

    assert valid_password(pwd, hashed_pwd)


def test_invalid_password():
    """Testing with an incorrect password."""

    pwd = "strongest_password_ever"
    hashed_pwd = hash_password(pwd)

    assert not valid_password("invalid_password", hashed_pwd)
