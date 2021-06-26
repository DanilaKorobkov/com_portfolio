import attr

from .entities import Portfolio
from .exceptions import MissingPortfolio, PortfolioAlreadyExists
from .repositories import PortfolioRepositoryInterface


@attr.s(auto_attribs=True, slots=True, frozen=True)
class PortfolioService:
    _portfolios: PortfolioRepositoryInterface

    async def get_portfolios(self) -> tuple[Portfolio, ...]:
        return await self._portfolios.find_all()

    async def get_portfolio(self, label: str) -> Portfolio:
        return await self._portfolios.find(label)

    async def create_portfolio_if_not_exists(self, label: str) -> None:
        await self._validate_not_exists(label)
        await self._portfolios.add(label)

    async def _validate_not_exists(self, label: str) -> None:
        try:
            await self.get_portfolio(label)
        except MissingPortfolio:
            pass
        else:
            raise PortfolioAlreadyExists
