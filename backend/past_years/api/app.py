import os
from typing import Any
from falcon import App, MEDIA_MSGPACK, MEDIA_JSON, CORSMiddleware


from past_years.api.handlers import JSONHandler
from past_years.api.middlewares import LogRequestMiddleware, CompressionMiddleware
from past_years.github.gh_client import GithubClient
from past_years.incorrect.incorrect_question import IncorrectQuestionsHandler
from past_years.search.factories import QuerySearcherFactory, QuestionBankFactory
from past_years.search.search_engine import QuestionSearchEngine
from past_years.configuration import config
from past_years.api.endpoints import QuestionsEndpoint, IncorrectQuestionEndpoint
from past_years.api.request import Request
from past_years.api.handlers import MsgPackHandler


def make_app() -> App:
    app = App(
        request_type=Request,
    )

    # Creating endpoints
    search_engine = _get_search_engine()
    incorrect_qstn_handler = _get_incorrect_question_handler()
    questions_endpoint = QuestionsEndpoint(search_engine)
    incorrect_question_endpoint = IncorrectQuestionEndpoint(incorrect_qstn_handler)

    # Adding routes
    app.add_route("/questions", questions_endpoint)
    app.add_route("/questions/random", questions_endpoint, suffix="random")
    app.add_route("/questions/metadata", questions_endpoint, suffix="metadata")
    app.add_route("/incorrect-question/{question_id}", incorrect_question_endpoint)

    # Adding handlers
    extra_media_handlers = {MEDIA_MSGPACK: MsgPackHandler(), MEDIA_JSON: JSONHandler()}
    app.resp_options.media_handlers.update(extra_media_handlers)

    # Adding middlewares
    middlewares = _get_middlwares()
    app.add_middleware(middlewares)

    return app


def _get_middlwares() -> list[Any]:
    """Configures the middleware and returns them."""

    api_config = config.get_api_config()
    cors_middleware = CORSMiddleware(
        allow_credentials="*",
        expose_headers=["X-Request-Id"],
        allow_origins=api_config.allow_origins,
    )

    middlewares = [cors_middleware, LogRequestMiddleware(), CompressionMiddleware()]
    return middlewares


def _get_incorrect_question_handler() -> IncorrectQuestionsHandler:

    pat: str = os.environ.get("GH_ISSUES_PAT")
    assert pat, f"PAT was {pat}"

    api_config = config.get_api_config()
    gh_client = GithubClient(pat, api_config.gh_repo_name, api_config.gh_repo_owner)

    return IncorrectQuestionsHandler(gh_client)


def _get_search_engine() -> QuestionSearchEngine:
    qb = QuestionBankFactory().get_question_bank("file")
    qs = QuerySearcherFactory().get_query_searcher("questions", "whoosh")

    return QuestionSearchEngine(qb, qs)
