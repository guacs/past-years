from falcon import Response

from past_years.api.request import Request
from past_years.auth.token_service import TokenServiceProtocol
from past_years.errors import InvalidTokenError


def authenticate_user(req: Request, resp: Response, _, __):
    auth_header: str | None = req.get_header("authorization")
    if not auth_header:
        raise Exception()

    token = auth_header.split(" ")[1]
    try:
        payload = TokenServiceProtocol.validate_access_token(token)
    except InvalidTokenError:
        raise Exception("invalid token")

    req.req_context.user_id = payload["user_id"]
