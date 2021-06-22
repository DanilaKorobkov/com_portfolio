from uuid import UUID

import attr

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
