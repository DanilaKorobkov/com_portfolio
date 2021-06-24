import attr

from com_portfolio.domain import Portfolio, PortfolioRepositoryInterface


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Application:
    _portfolios: PortfolioRepositoryInterface

    async def get_portfolios(self) -> tuple[Portfolio, ...]:
        return await self._portfolios.find_all()

    async def get_portfolio(self, label: str) -> Portfolio:
        return await self._portfolios.find(label)
