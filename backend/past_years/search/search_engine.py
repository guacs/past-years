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

    def search(self, filter: Filter) -> list[Question]:
        """Searches for questions based on the given filter."""

        hits = self._qbank.filter(filter)
        if filter.q:
            qsearch_hits = self._qsearcher.search(filter.q)
            hits.union(qsearch_hits)

        return list(self._qbank.get_questions(hits))

    def questions_metadata(self) -> QuestionsMetadata:
        """Returns the metadata regarding the questions."""

        return self._qbank.metadata
