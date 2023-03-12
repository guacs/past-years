"""A set of utilities related to authentication."""

import os
from hashlib import scrypt
from typing import NamedTuple

# ----- Password related helpers -----


class Password(NamedTuple):
    """The result being returned after creating a hash of a password."""

    hashed_password: bytes = b""
    salt: bytes = b""


def hash_password(password: str) -> Password:
    """Hashes the given password with a random salt."""

    salt = os.urandom(16)
    pwd_hash = _get_hash(password, salt)
    return Password(pwd_hash, salt)


def valid_password(password: str, hash_details: Password) -> bool:
    """Verifies the given password."""

    pwd_hash = _get_hash(password, hash_details.salt)
    return pwd_hash == hash_details.hashed_password


def _get_hash(password: str, salt: bytes) -> bytes:
    """Returns the hash for the given password with the given salt."""

    pwd_bytes = bytes(password, encoding="utf-8")
    return scrypt(pwd_bytes, salt=salt, n=16384, r=8, p=1)
