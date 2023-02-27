from __future__ import annotations

from pathlib import Path
from typing import Collection, Iterable, Iterator, Literal, Mapping, Type

import msgspec

from .search_types import Question, Filter, QuestionsIndex
from ..configuration import config


class QuestionBankProtocol(Mapping, Collection):
    """The question bank that holds all the questions and
    conducts the filtering."""

    def filter(self, filter_obj: Filter) -> Iterable[Question]:
        """Returns the questions that satisfy the given filter.

        NOTE: This does NOT consider the `q` or the query filter.
        """
        ...

    @classmethod
    def qb_factory(
        cls: Type[QuestionBankProtocol], type: Literal["file"]
    ) -> QuestionBankProtocol:
        """A factory method to get the appropriate QuestionBank instance.

        Args:
            type: The type of the question bank to get.
                file => `QuestionBank`
        """

        if type == "file":
            questions_config = config.get_questions_config()
            return QuestionBank(
                questions_config.questions_fp,
                questions_config.questions_index_fp
            )

        raise ValueError(f"{type} is an invalid value for `type`")


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
