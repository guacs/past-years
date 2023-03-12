from typing import Any

from dependency_injector.wiring import Provide, inject
from falcon import MEDIA_JSON, MEDIA_MSGPACK, App, CORSMiddleware

from past_years.api.dependencies import DepsContainer
from past_years.api.endpoints import IncorrectQuestionEndpoint, QuestionsEndpoint
from past_years.api.endpoints.login_endpoint import LoginEndpoint
from past_years.api.handlers import JSONHandler, MsgPackHandler
from past_years.api.middlewares import CompressionMiddleware, LogRequestMiddleware
from past_years.api.request import Request
from past_years.auth import TokenServiceProtocol
from past_years.configuration import config
from past_years.db.users_db import UsersDBProtocol
from past_years.incorrect.incorrect_question import IncorrectQuestionsHandler
from past_years.search.search_engine import QuestionSearchEngine


def make_app():
    """Creates the Falcon application instance."""

    @inject
    def _make_app(
        search_engine: QuestionSearchEngine = Provide[DepsContainer.search_engine],
        incorrect_qstn_handler: IncorrectQuestionsHandler = Provide[
            DepsContainer.incorrect_qstn
        ],
        user_db: UsersDBProtocol = Provide[DepsContainer.users_db],
        token_service: TokenServiceProtocol = Provide[DepsContainer.token_service],
    ) -> App:
        app = App(
            request_type=Request,
        )

        # Creating endpoints
        questions_endpoint = QuestionsEndpoint(search_engine)
        incorrect_question_endpoint = IncorrectQuestionEndpoint(incorrect_qstn_handler)
        login_endpoint = LoginEndpoint(user_db, token_service)

        # Adding routes
        app.add_route("/login", login_endpoint)
        app.add_route("/logout/{user_id}", login_endpoint, suffix="logout")
        app.add_route("/refresh", login_endpoint, suffix="refresh")

        app.add_route("/questions/{question_id}", questions_endpoint)
        app.add_route("/questions/filter", questions_endpoint, suffix="filter")
        app.add_route("/questions/random", questions_endpoint, suffix="random")
        app.add_route("/questions/metadata", questions_endpoint, suffix="metadata")

        app.add_route("/incorrect-question/{question_id}", incorrect_question_endpoint)

        # Adding handlers
        extra_media_handlers = {
            MEDIA_MSGPACK: MsgPackHandler(),
            MEDIA_JSON: JSONHandler(),
        }
        app.resp_options.media_handlers.update(extra_media_handlers)

        # Adding middlewares
        middlewares = _get_middlwares()
        app.add_middleware(middlewares)

        return app

    container = DepsContainer()
    container.wire([__name__])
    return _make_app()


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


# def _get_incorrect_question_handler() -> IncorrectQuestionsHandler:
#     pat: str = os.environ["GH_ISSUES_PAT"]
#     assert pat, f"PAT was {pat}"

#     api_config = config.get_api_config()
#     gh_client = GithubClient(pat, api_config.gh_repo_name, api_config.gh_repo_owner)

#     return IncorrectQuestionsHandler(gh_client)


# def _get_search_engine() -> QuestionSearchEngine:
#     qb = QuestionBankFactory().get_question_bank("file")
#     qs = QuerySearcherFactory().get_query_searcher("questions", "whoosh")

#     return QuestionSearchEngine(qb, qs)


# _db: MySqlDB | None = None


# def _get_users_db() -> UsersDBProtocol:
#     db = _get_db()
#     assert db is _db
#     return UsersDBMySql(db)


# def _get_token_service() -> TokenServiceProtocol:
#     db = _get_db()
#     assert db is _db
#     return TokenServiceMySql(db)


# def _get_db() -> MySqlDB:
#     global _db

#     if _db:
#         return _db

#     db_config = config.get_db_config()
#     _db = MySqlDB(db_config.db_name, db_config.host)
#     return _db
