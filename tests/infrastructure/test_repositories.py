import uuid

import aioredis
import pytest

from com_portfolio.context_vars import USER_ID, context_var_set
from com_portfolio.domain import (
    InvalidPortfolioLabel,
    Portfolio,
    PortfolioSchema,
)
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
        with context_var_set(USER_ID, user_id):
            assert await repository.find_all() == (portfolio,)

    async def test__find_all__user_has_no_portfolios(
        self,
        com_redis_client: aioredis.Redis,
    ) -> None:
        user_id = uuid.uuid4()

        repository = RedisPortfolioRepository(com_redis_client)
        with context_var_set(USER_ID, user_id):
            assert await repository.find_all() == tuple()

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
        with context_var_set(USER_ID, user_id):
            assert await repository.find(label) == portfolio

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
        with context_var_set(USER_ID, user_id):
            with pytest.raises(InvalidPortfolioLabel):
                await repository.find("missing_portfolio_label")

    async def test__find__user_has_no_portfolios(
        self,
        com_redis_client: aioredis.Redis,
    ) -> None:
        user_id = uuid.uuid4()

        repository = RedisPortfolioRepository(com_redis_client)
        with context_var_set(USER_ID, user_id):
            with pytest.raises(InvalidPortfolioLabel):
                await repository.find("portfolio_label")
