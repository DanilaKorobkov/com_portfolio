from http import HTTPStatus
from typing import Union

import ujson
from aiohttp import web


def make_json_response(
    body: Union[dict, list],
    status: int = HTTPStatus.OK,
) -> web.Response:
    return web.json_response(body, status=status, dumps=ujson.dumps)


def make_error_response(message: str, status: int) -> web.Response:
    body = {
        "message": message,
    }
    return make_json_response(body, status)
