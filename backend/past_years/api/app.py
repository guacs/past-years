from falcon import App, MEDIA_MSGPACK, MEDIA_JSON
from past_years.api.handlers import JSONHandler
from past_years.search.factories import QuerySearcherFactory, QuestionBankFactory

from past_years.search.search_engine import QuestionSearchEngine

from .endpoints import QuestionsEndpoint
from .request import Request
from .handlers import MsgPackHandler


def make_app() -> App:

    app = App(
        request_type=Request,
    )

    # Creating endpoints
    search_engine = _get_search_engine()
    questions_endpoint = QuestionsEndpoint(search_engine)

    # Adding routes
    app.add_route("/questions", questions_endpoint)

    # Adding handlers
    extra_media_handlers = {MEDIA_MSGPACK: MsgPackHandler(), MEDIA_JSON: JSONHandler()}
    app.resp_options.media_handlers.update(extra_media_handlers)

    return app


def _get_search_engine() -> QuestionSearchEngine:

    qb = QuestionBankFactory().get_question_bank("file")
    qs = QuerySearcherFactory().get_query_searcher("questions", "whoosh")

    return QuestionSearchEngine(qb, qs)
