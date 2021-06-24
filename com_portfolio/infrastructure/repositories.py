from collections import defaultdict
from typing import Iterable
from uuid import UUID

import aioredis
import attr

from com_portfolio.context_vars import USER_ID
from com_portfolio.domain import (
    InvalidPortfolioLabel,
    Portfolio,
    PortfolioRepositoryInterface,
    PortfolioSchema,
)

PortfolioByUserId = dict[UUID, dict[str, Portfolio]]


class FakePortfolioRepository(PortfolioRepositoryInterface):

    def __init__(
        self,
        user_portfolios: dict[UUID, Iterable[Portfolio]] = None,
    ) -> None:
        draft: dict = defaultdict(dict)

        if user_portfolios:
            for user_id, portfolios in user_portfolios.items():
                draft[user_id] = self._as_label_mapping(portfolios)

        self._portfolios = dict(draft)

    async def find_all(self) -> tuple[Portfolio, ...]:
        try:
            return tuple(
                self._portfolios[USER_ID.get()].values(),
            )
        except KeyError:
            return tuple()

    async def find(self, label: str) -> Portfolio:
        try:
            return self._portfolios[USER_ID.get()][label]
        except KeyError as e:
            raise InvalidPortfolioLabel from e

    @staticmethod
    def _as_label_mapping(
        portfolios: Iterable[Portfolio],
    ) -> dict[str, Portfolio]:
        return {
            portfolio.label: portfolio
            for portfolio in portfolios
        }


@attr.s(auto_attribs=True, slots=True, frozen=True)
class RedisPortfolioRepository(PortfolioRepositoryInterface):
    _redis: aioredis.Redis

    async def find_all(self) -> tuple[Portfolio, ...]:
        if user_portfolios := await self._redis.hgetall(str(USER_ID.get())):
            schema = PortfolioSchema()
            portfolios = list(user_portfolios.values())
            return tuple(schema.loads(portfolio) for portfolio in portfolios)
        return tuple()

    async def find(self, label: str) -> Portfolio:
        if raw := await self._redis.hget(str(USER_ID.get()), label):
            return PortfolioSchema().loads(raw)
        raise InvalidPortfolioLabel
