from typing import Any, NamedTuple

from loguru import logger

from past_years.github.gh_client import GithubClient


class CachedIssueDetails(NamedTuple):
    issue_number: int
    issue_url: str


class IncorrectQuestionsHandler:
    """A class to handle incorrect questions.

    Args:
        gh_client: The GitHub client.
    """

    def __init__(self, gh_client: GithubClient):
        self._gh = gh_client
        # This holds the question ID as the key and the
        # corresponding GitHub issue number
        self._cache: dict[str, CachedIssueDetails] = {}

    def get_question_issue_url(self, question_id: str) -> str | None:
        """Returns the URL to the GitHub issue for the given
        question id if it exists, else returns None."""

        cached_issue = self._cache.get(question_id, None)
        if cached_issue:
            return cached_issue.issue_url

        issue = self._get_issue(question_id)
        if not issue:
            return

        issue_url = issue["html_url"]
        self._cache[question_id] = CachedIssueDetails(issue["number"], issue_url)
        return issue_url

    def note_incorrect_question(self, question_id: str, comments: str) -> str:
        """Creates a new comment on an issue related to the question
        with the question ID.

        Returns:
            The URL of the new comment.
        """

        # 1. Check if an issue for the question already exists.
        #   a. If the issue exists:
        #       i. Add a comment to the issue
        #       ii. Reopen the issue if it's closed
        #   b. If the issue doesn't exist:
        #       i. Create an issue for the question
        #       ii. Add a comment to the issue
        logger.info(f"Creating comment for question `{question_id}`")

        issue = self._get_issue(question_id)
        if issue is not None:
            if issue["state"] != "open":
                pass  # TODO: Open the issue
        else:
            logger.debug(f"Creating issue for question `{question_id}`")

            issue_title = f"Incorrect Question: {question_id}"
            issue = self._gh.create_issue(issue_title, labels=["incorrect-question"])

        comment_details = self._add_comment(issue["number"], comments)
        return comment_details["html_url"]

    def _add_comment(self, issue_number: int, comments: str):
        """Adds the given comment to the issue."""

        comment = f"ISSUE NOTED BY USER\n\n{comments}\n\nSTATUS: Unresolved"
        return self._gh.create_issue_comment(issue_number, comment)

    def _get_issue(self, question_id: str) -> dict[str, Any] | None:
        """Returns an issue if it exists."""

        cached_issue = self._cache.get(question_id, None)
        if cached_issue:
            return self._gh.get_issue(cached_issue.issue_number)

        # The title is expected to be in the following format:
        # Incorrect Question: <question_id>
        for issue in self._gh.get_issues(labels=["incorrect-question"]):
            title = issue["title"]
            q_id = title.split(":")[-1].strip()
            self._cache[q_id] = CachedIssueDetails(issue["number"], issue["html_url"])
            if q_id == question_id:
                return issue
