from typing import TypedDict
from past_years.api.request import Request
from falcon import Response, HTTPNotFound, HTTPBadRequest

from past_years.incorrect import IncorrectQuestionsHandler
import msgspec

# ----- Constants -----

# The number of seconds for about 6 months
# i.e. seconds * mins * hours per day * days per month * months
ISSUE_URL_CACHE_TIME = 60 * 60 * 24 * 30 * 6


class IncorrectQuestionRequestBody(TypedDict):

    comments: str


class IncorrectQuestionEndpoint:
    """Handles all requests to /incorrect-question."""

    def __init__(self, incorrect_question_handler: IncorrectQuestionsHandler):

        self._incorrect_qstn_handler = incorrect_question_handler

    def on_get(self, req: Request, resp: Response, question_id: str):
        """Gets the issue url for the given question."""

        issue_url = self._incorrect_qstn_handler.get_question_issue_url(question_id)

        if not issue_url:
            raise HTTPNotFound(title="Issue not found")

        resp.media = issue_url
        # This can be safely cached for a loooong time
        resp.append_header("cache-control", f"public; max-age={ISSUE_URL_CACHE_TIME}")

    def on_post(self, req: Request, resp: Response, question_id: str):
        """Creating the new comments on the given question."""

        req_data = req.bounded_stream.read()
        try:
            req_body = msgspec.json.decode(req_data, type=IncorrectQuestionRequestBody)
        except msgspec.ValidationError:
            raise HTTPBadRequest("Invalid body")

        issue_url = self._incorrect_qstn_handler.note_incorrect_question(
            question_id, req_body["comments"]
        )

        resp.media = issue_url
