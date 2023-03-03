from typing import Generator, Iterable

import httpx
from typing import Any

from loguru import logger


class GithubClient:
    """A client to interact with GitHub via it's Rest API.

    Args:
        pat: The personal access token.
        base_url: The base url to which URLs in requests are added to.
            If provided, then all URIs provided during requests are
            considered to be relative.
    """

    def __init__(self, pat: str, repo: str, owner: str):
        self._repo, self._owner = repo, owner
        self._issues_url = f"/repos/{self._owner}/{self._repo}/issues"

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {pat}",
        }
        self._client = httpx.Client(base_url="https://api.github.com", headers=headers)

    # ----- Public Methods -----
    def get_issues(
        self, labels: Iterable[str] | None = None
    ) -> Generator[dict, None, None]:
        """Returns all the issues with the given label."""

        logger.debug("Getting all issues")

        query_params = None
        if labels:
            query_params = {"labels": ",".join(labels)}

        return self._paginate(self._issues_url, query_params)

    def get_issue(self, issue_number: int):
        """Returns the issue with the given issue number."""

        logger.debug(f"Getting issue `{issue_number}`")

        url = f"{self._issues_url}/{issue_number}"
        return self._get_request(url)

    def create_issue(self, title: str, body: str = "", labels: list[str] | None = None):
        """Creates a new issue with the given title and body."""

        logger.debug("Creating issue")

        params = {"title": title}
        if body:
            params["body"] = body
        if labels:
            params["labels"] = labels

        resp = self._post_request(self._issues_url, params)
        issue = resp.json()

        logger.debug(f"Created issue `{issue['id']}`")

        return issue

    def create_issue_comment(self, issue_number: int, comment: str):
        """Creates a comment on the issue with the given issue number."""

        logger.debug("Creating comment")

        body = {"body": comment}
        url = f"{self._issues_url}/{issue_number}/comments"
        return self._post_request(url, body).json()

    # ---- Private Methods ----
    def _paginate(
        self, url: str, params: dict[str, str] | None = None
    ) -> Generator[Any, None, None]:
        """Paginates a GitHub GET request."""

        while True:
            resp = self._get_request(url, params)

            # It's assumed that the response will be a list.
            resp_json = resp.json()
            for data in resp_json:
                yield data

            links = resp.headers.get_list("link", split_commas=True)
            # No pagination on this response
            if not links:
                break

            next_url = self._get_next_url(links)
            # No more pages to get
            if not next_url:
                break

            # Setting params to `None` since the
            # `next_url` already has the required query parameters
            url, params = next_url, None

    def _get_next_url(self, links: list[str]) -> str | None:
        """Gets the next url if it exists from the links header
        values from the response."""

        for link in links:
            if "next" in link:
                link = link.split(";")[0]
                return link.strip("<>")

    # --- Requests ---
    def _get_request(self, url: str, params: dict[str, str] | None = None):
        """Makes a get request and returns the response."""

        logger.trace(f"GET request to {url} with params {params}")

        resp = self._client.get(url, params=params)
        resp.raise_for_status()
        return resp

    def _post_request(self, url: str, params: dict[str, Any] | None = None):
        """Makes a post request and returns the response."""

        logger.trace(f"POST request to {url} with body {params}")

        resp = self._client.post(url, json=params)
        resp.raise_for_status()
        return resp
