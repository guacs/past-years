"""Tests all the factories in `search`."""
import pytest
from past_years.search import QuestionBankFactory, QuerySearcherFactory
from past_years.search.query_searcher import WhooshSearcher
from past_years.search.question_bank import QuestionBank


@pytest.fixture(scope="module")
def qb_factory() -> QuestionBankFactory:

    return QuestionBankFactory()


@pytest.fixture(scope="module")
def qs_factory() -> QuerySearcherFactory:

    return QuerySearcherFactory()


# ----- Testing QuestionBankFactory -----
def test_qb_factory_file(qb_factory: QuestionBankFactory):

    qb = qb_factory.get_question_bank("file")
    assert isinstance(qb, QuestionBank)


def test_qb_factory_invalid(qb_factory: QuestionBankFactory):

    with pytest.raises(ValueError):
        qb_factory.get_question_bank("invalid")  # type: ignore


# ----- Testing QuerySearcherFactory -----
def test_qs_factory(qs_factory: QuerySearcherFactory):

    qs = qs_factory.get_query_searcher("questions", "whoosh")
    assert isinstance(qs, WhooshSearcher)


def test_qs_factory_invalid(qs_factory: QuerySearcherFactory):

    with pytest.raises(ValueError):
        qs_factory.get_query_searcher("invalid", "whoosh")  # type: ignore

    with pytest.raises(ValueError):
        qs_factory.get_query_searcher("questions", "invalid")  # type: ignore
