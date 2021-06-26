from typing import Final

from aiohttp import web

from com_portfolio.application import Application

_APP_KEY: Final = "app"


def get_app(web_app: web.Application) -> Application:
    return web_app[_APP_KEY]


def set_app(web_app: web.Application, app: Application) -> None:
    web_app[_APP_KEY] = app
