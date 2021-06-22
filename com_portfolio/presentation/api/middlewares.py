from http import HTTPStatus

from aiohttp import web

from com_portfolio.application import InvalidAccessToken
from com_portfolio.domain import UserHasNoPortfolio

from .exceptions import InvalidAuthorizationHeader
from .responses import make_json_response
from .types import Handler


def register_middlewares(web_app: web.Application) -> None:
    web_app.middlewares.append(authorization_errors_middleware)
    web_app.middlewares.append(user_portfolio_errors_middleware)


@web.middleware
async def authorization_errors_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except (InvalidAuthorizationHeader, InvalidAccessToken) as e:
        raise web.HTTPUnauthorized from e  # DO: log warning


@web.middleware
async def user_portfolio_errors_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except UserHasNoPortfolio:
        response_body = {
            "message": "User has no portfolio",
        }
        return make_json_response(response_body, HTTPStatus.OK)
