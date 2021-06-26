from contextlib import asynccontextmanager
from typing import AsyncIterator

import attr

from com_portfolio.context_vars import USER_ID, context_var_set
from com_portfolio.domain import Portfolio, PortfolioService

from .identity_providers import IdentityProviderInterface


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Application:
    _portfolio_service: PortfolioService
    _identity_provider: IdentityProviderInterface

    async def get_portfolios(self, access_token: str) -> tuple[Portfolio, ...]:
        async with self._user_context(access_token):
            return await self._portfolio_service.get_portfolios()

    async def get_portfolio(self, access_token: str, label: str) -> Portfolio:
        async with self._user_context(access_token):
            return await self._portfolio_service.get_portfolio(label)

    async def create_portfolio(self, access_token: str, label: str) -> None:
        async with self._user_context(access_token):
            await self._portfolio_service.create_portfolio_if_not_exists(label)

    @asynccontextmanager
    async def _user_context(self, access_token: str) -> AsyncIterator[None]:
        user_id = await self._identity_provider.get_user_id(access_token)
        with context_var_set(var=USER_ID, value=user_id):
            yield
