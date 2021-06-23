import uuid

import aioredis
import pytest
import ujson

from com_portfolio.domain import Portfolio, UserHasNoPortfolio
from com_portfolio.infrastructure import RedisPortfolioRepository
from com_portfolio.test_utils import PortfolioFactory


class TestRedisPortfolioRepository:

    async def test__find__hit(self, com_redis_client: aioredis.Redis) -> None:
        portfolio: Portfolio = PortfolioFactory.build()
        portfolio_view = {
            "id": str(portfolio.id),
            "user_id": str(portfolio.user_id),
        }
        await com_redis_client.set(
            key=portfolio.user_id.hex,
            value=ujson.dumps(portfolio_view),
        )

        repository = RedisPortfolioRepository(com_redis_client)
        assert await repository.find(portfolio.user_id) == portfolio

    async def test__find__no_hit(
        self,
        com_redis_client: aioredis.Redis,
    ) -> None:
        missing_user_id = uuid.uuid4()
        repository = RedisPortfolioRepository(com_redis_client)

        with pytest.raises(UserHasNoPortfolio):
            await repository.find(missing_user_id)
