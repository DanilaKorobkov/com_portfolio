from typing import Final

from aiohttp import web

from com_portfolio.application import Application, IdentityProviderInterface

_APP_KEY: Final = "app"
_IDENTITY_PROVIDER_KEY = "identity_provider"


def get_app(web_app: web.Application) -> Application:
    return web_app[_APP_KEY]


def set_app(web_app: web.Application, app: Application) -> None:
    web_app[_APP_KEY] = app


def get_identity_provider(
    web_app: web.Application,
) -> IdentityProviderInterface:
    return web_app[_IDENTITY_PROVIDER_KEY]


def set_identity_provider(
    web_app: web.Application,
    identity_provider: IdentityProviderInterface,
) -> None:
    web_app[_IDENTITY_PROVIDER_KEY] = identity_provider
