"""Factory functions for various search objects."""

from typing import Literal

from loguru import logger

from ..configuration import config
from .query_searcher import QuerySearcherProtocol, WhooshSearcher
from .question_bank import QuestionBank, QuestionBankProtocol


class QuestionBankFactory:
    """A factory class to churn out question banks."""

    def get_question_bank(self, type: Literal["file"]) -> QuestionBankProtocol:
        """Returns a question bank based on the `type`."""

        logger.info(f"Getting question bank based on type `{type}`")

        if type == "file":
            questions_config = config.get_questions_config()
            return QuestionBank(
                questions_config.questions_fp, questions_config.questions_index_fp
            )

        raise ValueError(f"{type} is an invalid value for `type`")


class QuerySearcherFactory:
    """A factory class to churn out query searchers."""

    def get_query_searcher(
        self, document: Literal["questions"], type: Literal["whoosh"]
    ) -> QuerySearcherProtocol:
        """Returns a query searcher based on the values of `document`
        and `type`."""

        logger.info(
            f"Getting query searcher based on document `{document}` and type `{type}`"
        )

        if document == "questions":
            if type == "whoosh":
                qstn_config = config.get_questions_config()
                return WhooshSearcher(
                    str(qstn_config.whoosh_index_dir),
                    qstn_config.whoosh_questions_index_name,
                    qstn_config.whoosh_questions_field_name,
                )
            raise ValueError(f"'{type}' is an invalid value for type")

        raise ValueError(f"'{document}' is an invalid value for document")
