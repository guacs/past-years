from pathlib import Path
from typing import Generator

import pytest
from falcon.testing import TestClient

from past_years.api import make_app
from past_years.auth.token_service import TokenServiceMySql, TokenServiceProtocol
from past_years.configuration import config
from past_years.db import UsersDBMySql
from past_years.db.db import MySqlDB
from past_years.search.query_searcher import WhooshSearcher
from past_years.search.question_bank import QuestionBank
from past_years.search.search_engine import QuestionSearchEngine
from past_years.utils import configure_logger
from tests import setup
from tests.utils import MockUser

# This has to be done first, before running any other code.
config.mode = "test"
configure_logger()

# This is to ensure that the test database is setup for
# the API integration tests as well. I'm banking on the
# the database being dropped by the `teardown_database`
# function call in the cleanup code of the `db` fixture.
# Yes. It's a bit hacky.
# TODO: Figure out if there is a way to make a global setup/teardown.
setup.setup_database()

TEST_DATA_DIR = Path(__file__).parent / "data"
"""The path to the test data directory."""

# ----- API Related Fixtures -----


# NOTE: The scope is set to module so that the tables are all
# cleared and the new seed data is created.
@pytest.fixture(scope="module")
def client():
    setup.setup_database()
    setup.reset_table("users")
    app = make_app()
    return TestClient(app)


# ----- Questions Related Fixtures -----
@pytest.fixture(scope="session")
def question_bank() -> QuestionBank:
    """The file based question bank."""

    questions_fp = TEST_DATA_DIR / "questions.json"
    idx_fp = TEST_DATA_DIR / ".qindex.json"

    return QuestionBank(questions_fp, idx_fp)


@pytest.fixture(scope="session")
def whoosh_question_search_engine(question_bank: QuestionBank) -> QuestionSearchEngine:
    """The questions search engine."""

    whoosh_index_dir = TEST_DATA_DIR / "whoosh_index"
    whoosh_query_searcher = WhooshSearcher(
        str(whoosh_index_dir), "questions", "question"
    )

    return QuestionSearchEngine(question_bank, whoosh_query_searcher)


# ----- DB Related Fixtures -----
@pytest.fixture(scope="session")
def db() -> Generator[MySqlDB, None, None]:
    db_config = config.get_db_config()
    db = MySqlDB(db_config.db_name, db_config.host)
    yield db
    db.close()

    setup.teardown_database()


@pytest.fixture(scope="module")
def user_db(db: MySqlDB) -> UsersDBMySql:
    setup.reset_table("users")
    return UsersDBMySql(db)


@pytest.fixture(scope="module")
def token_service(db: MySqlDB) -> TokenServiceProtocol:
    setup.reset_table("tokens")
    return TokenServiceMySql(db)


@pytest.fixture
def existing_user() -> MockUser:
    """Returns a user that already exists in the database."""

    return MockUser("2", "Ankita", "ankita@yahoo.com", "ankita-password")
