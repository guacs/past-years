"""The types related to `search`."""

from dataclasses import dataclass
from enum import StrEnum
from typing import TypedDict
from msgspec import Struct


class Subject(StrEnum):
    """The various subjects."""

    ECONOMICS = "economics"
    ENVIRONMENT = "environment"
    POLITY = "polity"
    INTERNATIONAL_RELATIONS = "international relations"


class Exam(StrEnum):
    """All the various exams."""

    CSE = "CSE"
    CDS = "CDS"
    CAPF = "CAPF"
    NDA = "NDA"


class Question(Struct):
    """The representation of a single question."""

    main_question: str
    continuation: str
    question_options: list[str]
    answers: dict[str, str]
    correct_answer: str
    exam: Exam
    year: int
    subject: Subject
    id: str
    """The id of the question.

    This is the first 16 characters of the hexdigest i.e. 64 bits, of the
    SHA-1 hash of the `full_question`.
    """

    @property
    def full_question(self) -> str:
        """The full question.

        This is meant to be used for indexing purposes."""

        q_options = " ".join(self.question_options)
        answers = " ".join(self.answers.values())

        return f"{self.main_question} {self.continuation} {q_options} {answers}"

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Filter:
    """The filters to apply when conducting a search for the
    questions.

    All these filters are applied with 'AND' logic.
    """

    exams: tuple[Exam]
    """The exams to filter with (OR)."""

    subjects: tuple[Subject]
    """The subjects to filter with (OR)."""

    years: tuple[int]
    """The years to filter with (OR)."""

    q: str
    """The query to filter with (OR)."""


class QuestionsIndex(TypedDict):
    """The index with respect to exams, subjects and years
    for the questions.

    Each attribute holds a dictionary where the keys are the
    attribute value, and the corresponding value is a set of
    IDs of the questions that have that attribute value.
    """

    exams: dict[Exam, set[str]]
    subjects: dict[Subject, set[str]]
    years: dict[int, set[str]]
