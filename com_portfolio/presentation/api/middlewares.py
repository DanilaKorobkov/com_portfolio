import uuid
from http import HTTPStatus
from typing import Final

import inflection
from aiohttp import web

from com_portfolio.application import InvalidAccessToken
from com_portfolio.domain import InvalidPortfolioLabel
from com_portfolio.presentation.request_id import request_id_set

from .exceptions import InvalidAuthorizationHeader
from .responses import make_json_response
from .types import Handler

REQUEST_ID_HEADER: Final = "X-Request-ID"


def register_middlewares(web_app: web.Application) -> None:
    web_app.middlewares.append(request_id_middleware)
    web_app.middlewares.append(authorization_errors_middleware)
    web_app.middlewares.append(user_portfolio_errors_middleware)


@web.middleware
async def request_id_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    request_id = uuid.uuid4()

    with request_id_set(request_id):
        response = await handler(request)
        response.headers[REQUEST_ID_HEADER] = str(request_id)
    return response


@web.middleware
async def authorization_errors_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except (InvalidAuthorizationHeader, InvalidAccessToken) as e:
        message = humanize_exception(e)
        request.app.logger.info(message)

        response_body = {
            "message": message,
        }
        return make_json_response(response_body, HTTPStatus.UNAUTHORIZED)


@web.middleware
async def user_portfolio_errors_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except InvalidPortfolioLabel as e:
        response_body = {
            "message": humanize_exception(e),
        }
        return make_json_response(response_body, HTTPStatus.OK)


def humanize_exception(exc: Exception) -> str:
    return inflection.humanize(
        inflection.underscore(exc.__class__.__name__),
    )
