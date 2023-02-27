from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator, Protocol

import msgspec

from .search_types import Question, Filter, QuestionsIndex, QuestionsMetadata


class QuestionBankProtocol(Protocol):
    """The question bank that holds all the questions and
    conducts the filtering."""

    def filter(self, filter_obj: Filter) -> set[str]:
        """Returns the questions that satisfy the given filter.

        NOTE: This does NOT consider the `q` or the query filter.
        """
        ...

    def get_questions(self, ids: set[str]) -> Iterable[Question]:
        """Returns the questions that have the given IDs."""

        ...

    @property
    def metadata(self) -> QuestionsMetadata:
        """The metadata regarding the questions."""

        ...

    def __getitem__(self, id: str) -> Question:
        ...

    def __contains__(self, id: str) -> bool:
        ...

    def __iter__(self) -> Iterator[Question]:
        ...

    def __len__(self) -> int:
        ...


class QuestionBank(QuestionBankProtocol):
    """The question bank that holds all the questions and
    conducts the filtering.

    This loads all the questions from a file/directory and holds all
    the questions in memory.
    """

    def __init__(self, questions_fp: str | Path, questions_idx: str | Path):
        """
        Arguments:
            fp: The path to the file/directory that holds all the
            questions.

            questions_idx: The path to the questions index file.
        """

        questions_fp, idx_fp = Path(questions_fp), Path(questions_idx)

        self._questions = QuestionBank.load_questions(questions_fp)
        self._idx = msgspec.json.decode(idx_fp.read_bytes(), type=QuestionsIndex)
        self._metadata: QuestionsMetadata | None = None

    @property
    def metadata(self) -> QuestionsMetadata:

        if self._metadata is not None:
            return self._metadata

        exams, subjects, years = set(), set(), set()
        for q in self:
            exams.add(q.exam)
            subjects.add(q.subject)
            years.add(q.year)

        self._metadata = QuestionsMetadata(
            exams=exams, subjects=subjects, years=years, total_questions=len(self)
        )
        return self._metadata

    def get_questions(self, ids: set[str]) -> Iterable[Question]:
        return filter(lambda q: q.id in ids, iter(self))

    def filter(self, filter_obj: Filter) -> set[str]:
        raise NotImplementedError()

    # ----- Static Methods -----
    @staticmethod
    def load_questions(questions_fp: Path) -> dict[str, Question]:
        """Loads the questions from the given file.

        Args:
            questions_fp: The path to the file/directory with the
                questions.
        """
        questions: list[Question] = []
        if questions_fp.is_file():
            file_bytes = questions_fp.read_bytes()
            fp_questions = msgspec.json.decode(file_bytes, type=list[Question])
            questions.extend(fp_questions)

        for fp in questions_fp.rglob("*.json"):
            file_bytes = fp.read_bytes()
            fp_questions = msgspec.json.decode(file_bytes, type=list[Question])
            questions.extend(fp_questions)

        return {q.id: q for q in questions}

    # ----- Dunder Methods -----
    def __contains__(self, id: str) -> bool:
        return id in self._questions

    def __getitem__(self, id: str):
        return self._questions[id]

    def __iter__(self) -> Iterator[Question]:
        return iter(self._questions.values())

    def __len__(self) -> int:
        return len(self._questions)
