"""Utilities for testing."""

from typing import Generator, NamedTuple

from past_years.db.schemas import User


# ----- Types -----
class MockUser(NamedTuple):
    user_id: str
    display_name: str
    email: str
    password: str


# ----- Helper Functions -----
def _generate_user() -> Generator[User, None, None]:
    """Keeps on generating new users."""

    # This is needed to ensure that a new email is being
    # generated everytime without which an `IntegrityError`
    # is raised. The other option is to reseed the table before
    # each test, but that makes the tests too slow.

    name = "Guacs "
    count = 1
    while True:
        display_name = name + str(count)
        email = display_name + "@gmail.com"
        yield User(display_name, email)

        count += 1


generator = _generate_user()


def get_user() -> User:
    """Returns a new user."""

    return next(generator)
