from uuid import UUID

import aioredis
import attr
from marshmallow import Schema, fields, post_load

from com_portfolio.domain import (
    Portfolio,
    PortfolioRepositoryInterface,
    UserHasNoPortfolio,
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class FakePortfolioRepository(PortfolioRepositoryInterface):
    _portfolio_by_user_id: dict[UUID, Portfolio] = attr.Factory(dict)

    async def find(self, user_id: UUID) -> Portfolio:
        try:
            return self._portfolio_by_user_id[user_id]
        except KeyError as e:
            raise UserHasNoPortfolio from e


class _PortfolioSchema(Schema):
    id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)

    @post_load
    def release(self, data: dict, **_) -> Portfolio:
        return Portfolio(**data)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class RedisPortfolioRepository(PortfolioRepositoryInterface):
    _redis: aioredis.Redis
    _schema: _PortfolioSchema = attr.ib(init=False, default=_PortfolioSchema())

    async def find(self, user_id: UUID) -> Portfolio:
        if raw := await self._redis.get(key=user_id.hex, encoding="utf-8"):
            return self._schema.loads(raw)
        raise UserHasNoPortfolio
