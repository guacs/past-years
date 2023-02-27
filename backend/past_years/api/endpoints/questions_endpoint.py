from falcon import Response
from past_years.api.request import Request
from past_years.search import QuestionSearchEngine, Filter
import msgspec


class QuestionsEndpoint:
    """Handles all requests related to questions."""

    # The query parameter keys
    _EXAMS = "exams"
    _SUBJECTS = "subjects"
    _YEARS = "years"
    _QUERY = "q"
    _RANDOM_QUESTIONS_LIMIT = 5

    def __init__(self, search_engine: QuestionSearchEngine):

        self._search_engine = search_engine

    def on_get(self, req: Request, resp: Response):
        """Handles all requests for getting filtered questions."""

        filter = self._get_filter_object(req)
        resp.media = self._search_engine.search(filter)
        resp.content_type = req.get_accepted_content_type()

    def on_get_random(self, req: Request, resp: Response):
        """Handles all requests for getting random questions."""

        filter = self._get_filter_object(req)
        resp.media = self._search_engine.random(filter, self._RANDOM_QUESTIONS_LIMIT)
        resp.content_type = req.get_accepted_content_type()

    def on_get_metadata(self, req: Request, resp: Response):
        """Handles requests for getting the metadata of the questions."""

        resp.media = self._search_engine.questions_metadata()

    def _get_filter_object(self, req: Request) -> Filter:
        """Returns the filter object parsed from the request query string.

        If the default is provided and the filter object has no filters,
        then the default is returned, else the parsed filter object is returned.
        """

        def uppercase(s: str) -> str:
            return s.upper()

        def lowercase(s: str) -> str:
            return s.lower()

        filter_dict: dict[str, list[str] | str] = {}

        req.get_param(self._QUERY, store=filter_dict)
        req.get_param_as_list(self._EXAMS, store=filter_dict, transform=uppercase)
        req.get_param_as_list(self._SUBJECTS, store=filter_dict, transform=lowercase)
        req.get_param_as_list(self._YEARS, store=filter_dict, transform=int)

        try:
            filter_obj = msgspec.from_builtins(filter_dict, type=Filter)
            return filter_obj
        except msgspec.ValidationError as ex:
            error_msg = str(ex)
            if self._EXAMS in error_msg:
                param = self._EXAMS.title()
            elif self._SUBJECTS in error_msg:
                param = self._SUBJECTS.title()
            elif self._YEARS in error_msg:
                param = self._YEARS.title()
            else:
                param = "Query"

            raise Exception(param)
