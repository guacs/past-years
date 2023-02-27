from pathlib import Path
import pytest
from past_years.search.query_searcher import WhooshSearcher

from past_years.search.question_bank import QuestionBank
from past_years.search.search_engine import QuestionSearchEngine
from past_years.utils import configure_logger
from past_years.configuration import config

# This has to be done first, before running any other code.
config.mode = "test"
configure_logger()

TEST_DATA_DIR = Path(__file__).parent / "data"
"""The path to the test data directory."""


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
