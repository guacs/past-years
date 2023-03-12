import falcon
from falcon import HTTPBadRequest, Response

from past_years.api.request import Request
from past_years.auth import TokenServiceProtocol, valid_password
from past_years.db import UsersDBProtocol
from past_years.errors import InvalidTokenError, UserNotFoundError


class LoginEndpoint:
    _REQUIRED_DATA: tuple[str, str] = ("email", "password")

    def __init__(self, users_db: UsersDBProtocol, token_service: TokenServiceProtocol):
        self._user_db = users_db
        self._token_service = token_service

    def on_get_logout(self, request: Request, response: Response, user_id: str):
        self._token_service.delete_refresh_token(user_id)
        response.status = falcon.HTTP_200
        request.req_context.compress = False

    def on_post(self, request: Request, response: Response):
        """Handles logging in the user.

        Returns the user's data in the response and sets the created JWT
        as a cookie.
        """

        request.req_context.compress = False

        # Validating the request
        data: dict[str, str] = request.get_media()  # type: ignore
        if not all(d in data for d in self._REQUIRED_DATA):
            raise HTTPBadRequest(
                title="MissingData", description="Missing either email or password"
            )

        try:
            user = self._user_db.get_user_with_email(data["email"])
            pwd = self._user_db.get_user_password(user.user_id)
        except UserNotFoundError:
            response.status = falcon.HTTP_401
            return

        if not valid_password(data["password"], pwd):
            response.status = falcon.HTTP_401
            return

        access_token = self._token_service.create_jwt(user.user_id)
        refresh_token = self._token_service.get_refresh_token(user.user_id)
        if not refresh_token:
            refresh_token = self._token_service.create_refresh_token(user.user_id)

        response.media = {
            "refresh_token": refresh_token,
            "user": user,
            "access_token": access_token,
        }
        response.status = falcon.HTTP_200

    def on_post_refresh(self, request: Request, response: Response):
        """Gets a new access token from the given refresh token."""

        request.req_context.compress = False

        data: dict[str, str] = request.get_media()  # type: ignore
        refresh_token = data.get("token", "")
        if not refresh_token:
            raise HTTPBadRequest(
                title="MissingDetails", description="Refresh token is missing"
            )

        try:
            access_token = self._token_service.get_access_token_from_refresh_token(
                refresh_token
            )
        except InvalidTokenError:
            response.status = falcon.HTTP_401
            return

        response.status = falcon.HTTP_200
        response.media = access_token
