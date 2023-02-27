"""Handles all the indexing of the questions."""

from pathlib import Path
import time
from typing import Iterable
from loguru import logger
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import STORED, TEXT, Schema
from whoosh import index

import msgspec
from errors import IndexExistsError
from past_years.search.question_bank import QuestionBank
from past_years.search import Question
from past_years.search.search_types import QuestionsIndex


def create_questions_index(questions_fp: str | Path, idx_fp: str | Path) -> None:
    """Creates the questions index.

    Arguments:
        questions_fp: The path to the file/directory containing
            all the questions.
        idx_fp: The path to the questions index which is where the
            index will be saved to.
    """

    logger.info("Creating and saving the index")

    questions = _get_questions(questions_fp)
    idx = _create_questions_idx(questions)
    idx_bytes = msgspec.json.encode(idx)

    logger.debug("Saving the index")

    idx_fp = Path(idx_fp)
    idx_fp.write_bytes(idx_bytes)


def create_whoosh_index(
    idx_fp: str | Path, questions_fp: str | Path, questions_idx_name: str, reset: bool
) -> None:
    """Creates the Whoosh index for the questions.

    Arguments:
        idx_fp: The path to the directory where the
            index will be saved to.
        questions_fp: The path to the file/directory containing
            all the questions.
        questions_idx_name: The name of the questions index.
        reset: If `True`, then the existing index will
            be overwritten.
    """

    idx_fp = Path(idx_fp)
    if not reset and index.exists_in(str(idx_fp), questions_idx_name):
        raise IndexExistsError(questions_idx_name, idx_fp)
    elif not idx_fp.exists():
        logger.debug(f"Creating index directory at {idx_fp}")
        idx_fp.mkdir(parents=True)

    logger.info("Creating Whoosh index")
    schema = _get_whoosh_question_schema()
    idx = index.create_in(str(idx_fp), schema, questions_idx_name)

    writer = idx.writer()
    start_time = time.monotonic_ns()
    num_of_questions = 0

    for q in _get_questions(questions_fp):
        logger.trace(f"Indexing {q.id}")

        num_of_questions += 1
        writer.add_document(id=q.id, question=q.full_question)

    writer.commit()

    end_time = time.monotonic_ns()
    total_time = round((end_time - start_time) * 1e-6, 3)
    logger.info(f"Indexed {num_of_questions} questions in {total_time} ms")


# ----- Helpers -----
def _create_questions_idx(questions: Iterable[Question]) -> QuestionsIndex:
    """Creates and returns the questions index from the given questions."""

    logger.debug("Creating index")

    start_time = time.monotonic_ns()

    idx: QuestionsIndex = QuestionsIndex()
    num_of_questions = 0

    for q in questions:
        logger.trace(f"Indexing '{q.id}'")

        num_of_questions += 1

        exam_ids = idx.exams.setdefault(q.exam, set())
        subject_ids = idx.subjects.setdefault(q.subject, set())
        year_ids = idx.years.setdefault(q.year, set())

        for s in (exam_ids, subject_ids, year_ids):
            s.add(q.id)

    end_time = time.monotonic_ns()
    total_time = round((end_time - start_time) * 1e-6, 3)

    logger.info(f"Indexed {num_of_questions} questions in {total_time} ms")

    return idx


def _get_whoosh_question_schema() -> Schema:
    """Returns the schema used by the Whoosh index
    for questions."""

    question = TEXT(StemmingAnalyzer())
    return Schema(id=STORED, question=question)


def _get_questions(questions_fp: str | Path) -> Iterable[Question]:
    questions_fp = Path(questions_fp)

    logger.debug(f"Loading questions from {questions_fp}")

    return QuestionBank.load_questions(questions_fp).values()
