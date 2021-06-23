import uuid

import aioredis
import pytest

from com_portfolio.domain import Portfolio, PortfolioSchema, UserHasNoPortfolio
from com_portfolio.infrastructure import RedisPortfolioRepository
from com_portfolio.test_utils import PortfolioFactory, generate_portfolio_label


class TestRedisPortfolioRepository:

    async def test__find_all__hit(
        self,
        com_redis_client: aioredis.Redis,
    ) -> None:
        user_id = uuid.uuid4()
        label = generate_portfolio_label()

        portfolio: Portfolio = PortfolioFactory.build()
        await com_redis_client.hmset_dict(
            str(user_id),
            {
                label: PortfolioSchema().dumps(portfolio),
            },
        )

        repository = RedisPortfolioRepository(com_redis_client)
        assert await repository.find_all(user_id) == (portfolio,)

    async def test__find_all__user_has_no_portfolios(
        self,
        com_redis_client: aioredis.Redis,
    ) -> None:
        user_id = uuid.uuid4()

        repository = RedisPortfolioRepository(com_redis_client)
        assert await repository.find_all(user_id) == tuple()

    async def test__find__hit(self, com_redis_client: aioredis.Redis) -> None:
        user_id = uuid.uuid4()
        label = generate_portfolio_label()

        portfolio: Portfolio = PortfolioFactory.build()
        await com_redis_client.hmset_dict(
            str(user_id),
            {
                label: PortfolioSchema().dumps(portfolio),
            },
        )

        repository = RedisPortfolioRepository(com_redis_client)
        assert await repository.find(user_id, label) == portfolio

    async def test__find__invalid_portfolio_label(
        self,
        com_redis_client: aioredis.Redis,
    ) -> None:
        user_id = uuid.uuid4()
        label = generate_portfolio_label()

        portfolio: Portfolio = PortfolioFactory.build()
        await com_redis_client.hmset_dict(
            str(user_id),
            {
                label: PortfolioSchema().dumps(portfolio),
            },
        )

        repository = RedisPortfolioRepository(com_redis_client)
        with pytest.raises(UserHasNoPortfolio):
            await repository.find(user_id, label="missing_portfolio_label")

    async def test__find__user_has_no_portfolios(
        self,
        com_redis_client: aioredis.Redis,
    ) -> None:
        user_id = uuid.uuid4()

        repository = RedisPortfolioRepository(com_redis_client)
        with pytest.raises(UserHasNoPortfolio):
            await repository.find(user_id, label="portfolio_label")
