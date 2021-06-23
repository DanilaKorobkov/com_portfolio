import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, Final

import factory
from aiohttp.test_utils import TestClient, TestServer
from faker import Faker

from com_portfolio.application import Application
from com_portfolio.domain import Company, Portfolio, Position
from com_portfolio.presentation import api

_FAKER_RU: Final = Faker(locale="ru-RU")
_FAKER_EN: Final = Faker(locale="en-US")


@asynccontextmanager
async def api_client_factory(app: Application) -> AsyncIterator[TestClient]:
    web_app = api.create_web_app(app)

    async with TestServer(web_app) as server:
        async with TestClient(server) as client:
            yield client


def generate_company_ticker() -> str:
    return _FAKER_EN.word().upper()


def generate_position_count() -> int:
    return _FAKER_RU.pyint(min_value=1)


def generate_position_average_price() -> float:
    return _FAKER_RU.pyfloat(min_value=1, max_value=5000)


def generate_portfolio_label() -> str:
    return " ".join(_FAKER_RU.words())


def generate_portfolio_positions() -> tuple[Position, ...]:
    size = _FAKER_RU.random_int(5, 25)
    return tuple(
        PositionFactory.build() for _ in range(size)
    )


class CompanyFactory(factory.Factory):

    class Meta:
        model = Company

    ticker = factory.LazyFunction(generate_company_ticker)


class PositionFactory(factory.Factory):

    class Meta:
        model = Position

    company = factory.SubFactory(CompanyFactory)
    count = factory.LazyFunction(generate_position_count)
    average_price = factory.LazyFunction(generate_position_average_price)


class PortfolioFactory(factory.Factory):

    class Meta:
        model = Portfolio

    id = factory.LazyFunction(uuid.uuid4)
    label = factory.LazyFunction(generate_portfolio_label)
    positions = factory.LazyFunction(generate_portfolio_positions)
