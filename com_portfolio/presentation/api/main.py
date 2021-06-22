from aiohttp import web

from com_portfolio.application import Application
from com_portfolio.infrastructure import (
    FakeIdentityProvider,
    FakePortfolioRepository,
)
from com_portfolio.presentation import api


def main() -> None:
    web.run_app(create_app(), port=8081)


async def create_app() -> web.Application:
    app = Application(
        FakeIdentityProvider(),
        FakePortfolioRepository(),
    )
    return api.create_web_app(app)
