import uuid
from http import HTTPStatus
from typing import Final

import inflection
from aiohttp import web

from com_portfolio.application import InvalidAccessToken
from com_portfolio.context_vars import REQUEST_ID, USER_ID, context_var_set
from com_portfolio.domain import InvalidPortfolioLabel

from .exceptions import InvalidAuthorizationHeader
from .helpers import get_identity_provider
from .responses import make_error_response, make_json_response
from .types import Handler

REQUEST_ID_HEADER: Final = "X-Request-ID"


def register_middlewares(web_app: web.Application) -> None:
    web_app.middlewares.append(request_id_middleware)
    web_app.middlewares.append(authorization_middleware)
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
async def authorization_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    identity_provider = get_identity_provider(request.app)
    try:
        access_token = _get_access_token(request)
        user_id = await identity_provider.get_user_id(access_token)
    except (InvalidAuthorizationHeader, InvalidAccessToken) as e:
        message = _humanize_exception(e)
        request.app.logger.info(message)
        return make_error_response(message, HTTPStatus.UNAUTHORIZED)
    else:
        with context_var_set(var=USER_ID, value=user_id):
            return await handler(request)


@web.middleware
async def user_portfolio_errors_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except InvalidPortfolioLabel as e:
        response_body = {
            "message": _humanize_exception(e),
        }
        return make_json_response(response_body, HTTPStatus.OK)


def _get_access_token(request: web.Request) -> str:
    try:
        _, token = request.headers['Authorization'].strip().split()
    except (KeyError, ValueError) as e:
        raise InvalidAuthorizationHeader from e
    else:
        return token


def _humanize_exception(exc: Exception) -> str:
    return inflection.humanize(
        inflection.underscore(exc.__class__.__name__),
    )
