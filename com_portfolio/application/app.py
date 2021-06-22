import attr

from com_portfolio.domain import Portfolio, PortfolioRepositoryInterface

from .identity_provider import IdentityProviderInterface


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Application:
    _identity_provider: IdentityProviderInterface
    _portfolios: PortfolioRepositoryInterface

    async def get_portfolio(self, access_token: str) -> Portfolio:
        user_id = await self._identity_provider.get_user_id(access_token)
        return await self._portfolios.find(user_id)
