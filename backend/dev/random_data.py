from hashlib import sha1
from pathlib import Path
from random import choice, choices, randint
from typing import Generator

import msgspec
from msgspec import Struct

from past_years.search.question_bank import QuestionBank
from past_years.search.search_types import Exam, Question, Subject


class RandomQuestionGenerator:
    """A class to create random questions."""

    def __init__(self, total_questions: int = 100, words_fp: str | Path = ""):
        self.total_questions = total_questions

        if words_fp:
            words_fp = Path(words_fp)
        else:
            words_fp = Path(__file__).parent / "random_data.json"
        self._data = msgspec.json.decode(
            words_fp.read_bytes(), type=RandomDataPopulation
        )

    def create_questions(self) -> Generator[Question, None, None]:
        """Yields a single question."""

        answer_choices = ["A", "B", "C", "D"]
        exams, subjects = list(Exam), list(Subject)
        years = list(range(2015, 2023))

        for _ in range(self.total_questions):
            question = Question(
                self._get_main_question(),
                self._get_continuation(),
                self._get_question_options(),
                self._return_answers(),
                choice(answer_choices),
                choice(exams),
                choice(years),
                choice(subjects),
                "",
            )
            question.id = self._get_question_hash(question)

            yield question

    # ----- Private Methods -----
    def _get_main_question(self) -> str:
        n = randint(3, 6)
        sentences = choices(self._data.main_question_sentences, k=n)
        return " ".join(sentences)

    def _get_continuation(self) -> str:
        return choice(self._data.continuation)

    def _get_question_options(self) -> list[str]:
        n = randint(0, 4)
        return choices(self._data.question_options, k=n)

    def _return_answers(self) -> dict[str, str]:
        return {
            "a": choice(self._data.answers),
            "b": choice(self._data.answers),
            "c": choice(self._data.answers),
            "d": choice(self._data.answers),
        }

    def _get_question_hash(self, q: Question) -> str:
        full_question = bytes(q.full_question, encoding="utf-8")
        sha_hash = sha1(full_question, usedforsecurity=False)
        return sha_hash.hexdigest()[:16]


class RandomDataPopulation(Struct):
    main_question_sentences: list[str] = []
    continuation: list[str] = []
    question_options: list[str] = []
    answers: list[str] = []


def regenerate_random_data(questions_fp: str | Path):
    questions = QuestionBank.load_questions(Path(questions_fp))
    rand_data = RandomDataPopulation()
    for q in questions.values():
        main_q = q.main_question.split(".")
        rand_data.main_question_sentences.extend(main_q)

        continuation = q.continuation.split(".")
        rand_data.continuation.extend(continuation)

        rand_data.question_options.extend(q.question_options)
        rand_data.answers.extend(q.answers.values())

    fp = Path("/home/guacs/projects/past-years/backend/dev/random_data.json")
    fp.write_bytes(msgspec.json.encode(rand_data))
