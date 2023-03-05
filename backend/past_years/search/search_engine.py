import itertools
from math import exp, floor, log
from random import random, randrange
from typing import Iterable
from past_years.errors import QuestionNotFoundError
from past_years.search.query_searcher import QuerySearcherProtocol
from past_years.search.question_bank import QuestionBankProtocol
from past_years.search.search_types import Filter, Question, QuestionsMetadata


class QuestionSearchEngine:
    """A search engine for the questions."""

    def __init__(
        self, question_bank: QuestionBankProtocol, query_searcher: QuerySearcherProtocol
    ):
        self._qbank = question_bank
        self._qsearcher = query_searcher

    def get_question(self, question_id: str) -> Question:
        """Returns the question with the given question id."""

        try:
            return self._qbank[question_id]
        except KeyError as ex:
            raise QuestionNotFoundError(question_id) from ex

    def search(self, filter: Filter) -> list[Question]:
        """Searches for questions based on the given filter."""

        hits = self._search(filter)
        return list(self._qbank.get_questions(hits))

    def random(self, filter: Filter, n: int = 100) -> list[Question]:
        """Returns a random set of questions that satisfy the given
        filter.

        Args:
            filter: The filter to apply on the questions.
            n: The number of questions to return.
        """

        hits = self._search(filter)
        questions = self._qbank.get_questions(hits)
        return self._sample_random(questions, n)

    def questions_metadata(self) -> QuestionsMetadata:
        """Returns the metadata regarding the questions."""

        return self._qbank.metadata

    def _sample_random(self, questions: Iterable[Question], k: int):
        # This implementation is essentially an exact copy of the
        # implementation in `more-itertools` which itself is based on
        # `Algorithm L` from the paper
        # "Reservoir-Sampling Algorithms of Time Complexity O(n(1+log(N/n)))"
        # by Kim-Hung Li.
        # Implementation reference:
        # https://github.com/more-itertools/more-itertools/blob/474b6a5b39a3fa7642f8b472954e4eac3c1a78b8/more_itertools/more.py#L3454

        # Filling up the reservoir with the first 'k' items
        reservoir = list(itertools.islice(questions, k))

        W = exp(log(random()) / k)
        next_index = k + floor(log(random()) / log(1 - W))

        try:
            for index, element in enumerate(questions, k):
                if index == next_index:
                    reservoir[randrange(k)] = element
                    W *= exp(log(random()) / k)
                    next_index += floor(log(random()) / log(1 - W)) + 1
        except IndexError:
            # IndexError happens if k < len(questions)
            return list(questions)

        return reservoir

    def _search(self, filter: Filter) -> set[str]:
        hits = self._qbank.filter(filter)
        if filter.q:
            qsearch_hits = self._qsearcher.search(filter.q)
            hits.union(qsearch_hits)

        return hits
