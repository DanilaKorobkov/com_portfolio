from http import HTTPStatus
from typing import Union

import ujson
from aiohttp import web


def make_json_response(
    body: Union[dict, list],
    status: int = HTTPStatus.OK,
) -> web.Response:
    return web.json_response(body, status=status, dumps=ujson.dumps)
