from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator, Protocol

import msgspec

from .search_types import (
    Exam,
    Question,
    Filter,
    QuestionsIndex,
    QuestionsMetadata,
    Subject,
)
from loguru import logger


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

        self._metadata: QuestionsMetadata | None = None
        self._questions = QuestionBank.load_questions(questions_fp)
        self._all_ids: set[str] = set(self._questions.keys())

        logger.debug(f"Loading index from `{idx_fp}`")
        self._idx = msgspec.json.decode(idx_fp.read_bytes(), type=QuestionsIndex)

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

        logger.debug(f"Filter with filter: {filter_obj}")

        filtered_ids: set[str] = self._all_ids
        if filter_obj.exams:
            exam_ids = self._filter_by_exams(filter_obj.exams)
            filtered_ids = filtered_ids.intersection(exam_ids)
        if filter_obj.subjects:
            subject_ids = self._filter_by_subjects(filter_obj.subjects)
            filtered_ids = filtered_ids.intersection(subject_ids)
        if filter_obj.years:
            year_ids = self._filter_by_year(filter_obj.years)
            filtered_ids = filtered_ids.intersection(year_ids)

        return filtered_ids

    # ----- Private Methods -----
    def _filter_by_exams(self, exams: Iterable[Exam]) -> set[str]:
        logger.trace(f"Filter by exams: {exams}")

        all_exams: set[str] = set()
        for exam in exams:
            all_exams |= self._idx.exams[exam]
        return all_exams

    def _filter_by_subjects(self, subjects: Iterable[Subject]) -> set[str]:
        logger.trace(f"Filter by subjects: {subjects}")

        all_subjects: set[str] = set()
        for subject in subjects:
            all_subjects |= self._idx.subjects[subject]
        return all_subjects

    def _filter_by_year(self, years: Iterable[int]) -> set[str]:
        logger.trace(f"Filter by years: {years}")

        all_years: set[str] = set()
        for year in years:
            all_years |= self._idx.years[year]
        return all_years

    # ----- Static Methods -----
    @staticmethod
    def load_questions(questions_fp: Path) -> dict[str, Question]:
        """Loads the questions from the given file.

        Args:
            questions_fp: The path to the file/directory with the
                questions.
        """

        logger.debug(f"Loading questions from `{questions_fp}`")

        questions: list[Question] = []
        if questions_fp.is_file():
            file_bytes = questions_fp.read_bytes()
            fp_questions = msgspec.json.decode(file_bytes, type=list[Question])
            questions.extend(fp_questions)
        else:
            for fp in questions_fp.rglob("*.json"):

                logger.trace(f"Loading questions from `{fp}`")

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
