from aiohttp import web

from com_portfolio.application import Application

from .helpers import set_app
from .middlewares import register_middlewares
from .views import register_views


def create_web_app(app: Application) -> web.Application:
    web_app = web.Application()

    register_views(web_app)
    register_middlewares(web_app)

    set_app(web_app, app)

    return web_app
