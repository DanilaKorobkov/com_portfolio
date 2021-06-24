from aiohttp import web

from com_portfolio.application import Application, IdentityProviderInterface

from .helpers import set_app, set_identity_provider
from .middlewares import register_middlewares
from .views import register_views


def create_web_app(
    app: Application,
    identity_provider: IdentityProviderInterface,
) -> web.Application:
    web_app = web.Application()

    register_views(web_app)
    register_middlewares(web_app)

    set_app(web_app, app)
    set_identity_provider(web_app, identity_provider)

    return web_app
