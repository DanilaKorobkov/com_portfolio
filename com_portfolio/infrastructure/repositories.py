import uuid
from collections import defaultdict
from typing import Iterable, Mapping
from uuid import UUID

import aioredis
import attr

from com_portfolio.context_vars import USER_ID
from com_portfolio.domain import (
    MissingPortfolio,
    Portfolio,
    PortfolioRepositoryInterface,
    PortfolioSchema,
)

PortfolioByUserId = dict[UUID, dict[str, Portfolio]]


class FakePortfolioRepository(PortfolioRepositoryInterface):

    def __init__(
        self,
        user_portfolios: Mapping[UUID, Iterable[Portfolio]] = None,
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
            raise MissingPortfolio from e

    async def add(self, label: str) -> UUID:
        portfolio = Portfolio(
            id=uuid.uuid4(),
            label=label,
        )
        user_portfolios = self._portfolios.setdefault(USER_ID.get(), {})
        user_portfolios[label] = portfolio
        return portfolio.id

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
        # pylint: disable=fixme
        # TODO: transaction

        user_keys_pattern = f"{self._get_user_key_prefix()}:*"
        user_keys = await self._redis.keys(user_keys_pattern)
        if not user_keys:
            return tuple()

        dumps = await self._redis.mget(*user_keys)
        schema = PortfolioSchema()
        return tuple(schema.loads(dump) for dump in dumps)

    async def find(self, label: str) -> Portfolio:
        key = self._get_key(label)
        if dump := await self._redis.get(key):
            return PortfolioSchema().loads(dump)
        raise MissingPortfolio

    async def add(self, label: str) -> UUID:
        portfolio = Portfolio(
            id=uuid.uuid4(),
            label=label,
        )
        dump = PortfolioSchema().dumps(portfolio)
        await self._redis.set(self._get_key(label), dump)
        return portfolio.id

    @staticmethod
    def _get_key(label: str) -> str:
        return f"{RedisPortfolioRepository._get_user_key_prefix()}:{label}"

    @staticmethod
    def _get_user_key_prefix() -> str:
        return str(USER_ID.get())
