"""A set of DB schemas."""


from dataclasses import dataclass


@dataclass
class User:
    """Represents a user stored within the database."""

    display_name: str
    email: str
    user_id: str = ""
