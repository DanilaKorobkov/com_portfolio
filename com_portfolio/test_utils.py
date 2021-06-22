import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, Final

import factory
from aiohttp.test_utils import TestClient, TestServer
from faker import Faker

from com_portfolio.application import Application
from com_portfolio.domain import Portfolio
from com_portfolio.presentation import api

_FAKER: Final = Faker(locale="ru-RU")


@asynccontextmanager
async def api_client_factory(app: Application) -> AsyncIterator[TestClient]:
    web_app = api.create_web_app(app)

    async with TestServer(web_app) as server:
        async with TestClient(server) as client:
            yield client


class PortfolioFactory(factory.Factory):

    class Meta:
        model = Portfolio

    id = factory.LazyFunction(uuid.uuid4)
    user_id = factory.LazyFunction(uuid.uuid4)
