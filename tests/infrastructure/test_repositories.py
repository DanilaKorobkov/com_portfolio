from uuid import UUID

import aioredis
import pytest

from com_portfolio.domain import MissingPortfolio, Portfolio, PortfolioSchema
from com_portfolio.infrastructure import (
    FakePortfolioRepository,
    RedisPortfolioRepository,
)
from com_portfolio.test_utils import PortfolioFactory, generate_portfolio_label


class TestFakePortfolioRepository:

    async def test__find_all__hit(self, user_id: UUID) -> None:
        portfolios: list[Portfolio] = PortfolioFactory.build_batch(size=2)
        user_portfolios = {
            user_id: portfolios,
        }
        repository = FakePortfolioRepository(user_portfolios)

        assert await repository.find_all() == tuple(portfolios)

    async def test__find_all__user_has_no_portfolios(
        self,
        user_id: UUID,
    ) -> None:
        repository = FakePortfolioRepository()
        assert await repository.find_all() == tuple()

    async def test__find__hit(self, user_id: UUID) -> None:
        portfolio: Portfolio = PortfolioFactory.build()
        user_portfolios = {
            user_id: [portfolio],
        }
        repository = FakePortfolioRepository(user_portfolios)

        assert await repository.find(portfolio.label) == portfolio

    async def test__find__invalid_portfolio_label(self, user_id: UUID) -> None:
        portfolio: Portfolio = PortfolioFactory.build()
        user_portfolios = {
            user_id: [portfolio],
        }
        repository = FakePortfolioRepository(user_portfolios)

        with pytest.raises(MissingPortfolio):
            await repository.find("missing_portfolio_label")

    async def test__find__user_has_no_portfolios(self, user_id: UUID) -> None:
        repository = FakePortfolioRepository()

        with pytest.raises(MissingPortfolio):
            await repository.find("portfolio_label")

    async def test__add__new_portfolio(self, user_id: UUID) -> None:
        repository = FakePortfolioRepository()

        label = generate_portfolio_label()

        await repository.add(label)
        assert (await repository.find(label)).label == label

    async def test__add__exists_portfolio__override(
        self,
        user_id: UUID,
    ) -> None:
        portfolio: Portfolio = PortfolioFactory.build()
        user_portfolios = {
            user_id: [portfolio],
        }
        repository = FakePortfolioRepository(user_portfolios)

        await repository.add(portfolio.label)
        assert (await repository.find(portfolio.label)).id != portfolio.id


class TestRedisPortfolioRepository:

    async def test__find_all__hit(
        self,
        user_id: UUID,
        com_redis_client: aioredis.Redis,
    ) -> None:
        label = generate_portfolio_label()

        portfolio: Portfolio = PortfolioFactory.build()
        await com_redis_client.hmset_dict(
            str(user_id),
            {
                label: PortfolioSchema().dumps(portfolio),
            },
        )

        repository = RedisPortfolioRepository(com_redis_client)
        assert await repository.find_all() == (portfolio,)

    async def test__find_all__user_has_no_portfolios(
        self,
        user_id: UUID,
        com_redis_client: aioredis.Redis,
    ) -> None:
        repository = RedisPortfolioRepository(com_redis_client)
        assert await repository.find_all() == tuple()

    async def test__find__hit(
        self,
        user_id: UUID,
        com_redis_client: aioredis.Redis,
    ) -> None:
        label = generate_portfolio_label()

        portfolio: Portfolio = PortfolioFactory.build()
        await com_redis_client.hmset_dict(
            str(user_id),
            {
                label: PortfolioSchema().dumps(portfolio),
            },
        )

        repository = RedisPortfolioRepository(com_redis_client)
        assert await repository.find(label) == portfolio

    async def test__find__invalid_portfolio_label(
        self,
        user_id: UUID,
        com_redis_client: aioredis.Redis,
    ) -> None:
        label = generate_portfolio_label()

        portfolio: Portfolio = PortfolioFactory.build()
        await com_redis_client.hmset_dict(
            str(user_id),
            {
                label: PortfolioSchema().dumps(portfolio),
            },
        )

        repository = RedisPortfolioRepository(com_redis_client)
        with pytest.raises(MissingPortfolio):
            await repository.find("missing_portfolio_label")

    async def test__find__user_has_no_portfolios(
        self,
        user_id: UUID,
        com_redis_client: aioredis.Redis,
    ) -> None:
        repository = RedisPortfolioRepository(com_redis_client)
        with pytest.raises(MissingPortfolio):
            await repository.find("portfolio_label")

    async def test__add__create_new(
        self,
        user_id: UUID,
        com_redis_client: aioredis.Redis,
    ) -> None:
        label = generate_portfolio_label()

        repository = RedisPortfolioRepository(com_redis_client)

        await repository.add(label)
        assert (await repository.find(label)).label == label

    async def test__add__override(
        self,
        user_id: UUID,
        com_redis_client: aioredis.Redis,
    ) -> None:
        label = generate_portfolio_label()

        repository = RedisPortfolioRepository(com_redis_client)

        portfolio_id = await repository.add(label)
        assert await repository.add(label) != portfolio_id
