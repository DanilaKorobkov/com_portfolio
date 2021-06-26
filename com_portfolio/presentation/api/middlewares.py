import uuid
from http import HTTPStatus
from typing import Final

import inflection
from aiohttp import web

from com_portfolio.application import InvalidAccessToken
from com_portfolio.context_vars import REQUEST_ID, context_var_set
from com_portfolio.domain import MissingPortfolio, PortfolioAlreadyExists

from .exceptions import InvalidAuthorizationHeader
from .responses import make_error_response
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

    with context_var_set(var=REQUEST_ID, value=request_id):
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
        message = _humanize_exception(e)
        request.app.logger.info(message)
        return make_error_response(message, HTTPStatus.UNAUTHORIZED)


@web.middleware
async def user_portfolio_errors_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except (MissingPortfolio, PortfolioAlreadyExists) as e:
        message = _humanize_exception(e)
        return make_error_response(message, HTTPStatus.BAD_REQUEST)


def _humanize_exception(exc: Exception) -> str:
    return inflection.humanize(
        inflection.underscore(exc.__class__.__name__),
    )
