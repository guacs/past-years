from typing import Iterable

from past_years.search import Exam, Question, Subject
from past_years.search.question_bank import QuestionBank
from past_years.search.search_types import Filter

# ----- Helpers -----


def check_exams(questions: Iterable[Question], exams: list[Exam]) -> bool:
    """Checks that all the questions' exam is one of the given exams."""

    return all(q.exam in exams for q in questions)


def check_subjects(questions: Iterable[Question], subjects: list[Subject]) -> bool:
    return all(q.subject in subjects for q in questions)


def check_years(questions: Iterable[Question], years: list[int]) -> bool:
    return all(q.year in years for q in questions)


def check_all_questions(all_questions: Iterable[Question], questions: list[Question]):
    all_questions = list(all_questions)

    assert len(all_questions) == len(questions)

    for q in all_questions:
        assert q in questions


# ----- Tests -----


def test_filter_by_subject(question_bank: QuestionBank):
    subjects = [Subject.POLITY, Subject.ECONOMICS]
    question_ids = question_bank._filter_by_subjects(subjects)
    questions = list(question_bank.get_questions(question_ids))

    assert check_subjects(questions, subjects) is True

    # Checking that all questions with the given subjects is found
    all_questions = list(filter(lambda q: q.subject in subjects, iter(question_bank)))
    assert len(questions) == len(all_questions)
    for q in all_questions:
        assert q in questions


def test_filter_by_exams(question_bank: QuestionBank):
    exams = [Exam.CSE]
    question_ids = question_bank._filter_by_exams(exams)
    questions = list(question_bank.get_questions(question_ids))

    assert check_exams(questions, exams) is True

    # Checking that all questions with the given exams is found
    all_questions = filter(lambda q: q.exam in exams, iter(question_bank))
    check_all_questions(all_questions, questions)


def test_filter_by_years(question_bank: QuestionBank):
    years = [2021, 2020]
    question_ids = question_bank._filter_by_year(years)
    questions = list(question_bank.get_questions(question_ids))

    assert check_years(questions, years) is True

    # Checking that all questions with the given years is found
    all_questions = filter(lambda q: q.year in years, iter(question_bank))
    check_all_questions(all_questions, questions)


def test_filter(question_bank: QuestionBank):
    filters = Filter(
        exams=[Exam.CDS],
        subjects=[Subject.ENVIRONMENT, Subject.INTERNATIONAL_RELATIONS],
        years=[2020, 2022],
    )

    questions = list(question_bank.get_questions(question_bank.filter(filters)))

    assert check_exams(questions, filters.exams) is True
    assert check_subjects(questions, filters.subjects) is True
    assert check_years(questions, filters.years) is True

    def predicate(q: Question) -> bool:
        return (
            q.exam in filters.exams
            and q.year in filters.years
            and q.subject in filters.subjects
        )

    all_questions = filter(predicate, iter(question_bank))
    check_all_questions(all_questions, questions)


def test_partial_filter(question_bank: QuestionBank):
    # Creating a filter without exams i.e. a partial filter
    filters = Filter(subjects=[Subject.ECONOMICS, Subject.POLITY], years=[2022, 2021])

    questions = list(question_bank.get_questions(question_bank.filter(filters)))

    assert check_subjects(questions, filters.subjects)
    assert check_years(questions, filters.years)

    def predicate(q: Question) -> bool:
        return q.year in filters.years and q.subject in filters.subjects

    all_questions = filter(predicate, iter(question_bank))
    check_all_questions(all_questions, questions)
