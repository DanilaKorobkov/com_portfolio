import secrets
import uuid
from http import HTTPStatus

from com_portfolio.application import Application
from com_portfolio.infrastructure import (
    FakeIdentityProvider,
    FakePortfolioRepository,
)
from com_portfolio.test_utils import PortfolioFactory, api_client_factory


class TestPortfolioView:

    async def test__hit(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        portfolio = PortfolioFactory.build(user_id=user_id)
        app = Application(
            FakeIdentityProvider(
                user_id_by_token={
                    access_token: user_id,
                },
            ),
            FakePortfolioRepository(
                portfolio_by_user_id={
                    user_id: portfolio,
                },
            ),
        )
        async with api_client_factory(app) as client:
            response = await client.get(
                "/portfolio",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK
            assert await response.json() == {
                "portfolio": {
                    "id": str(portfolio.id),
                    "user_id": str(portfolio.user_id),
                },
            }

    async def test__missing_authorization_header(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        portfolio = PortfolioFactory.build(user_id=user_id)
        app = Application(
            FakeIdentityProvider(
                user_id_by_token={
                    access_token: user_id,
                },
            ),
            FakePortfolioRepository(
                portfolio_by_user_id={
                    user_id: portfolio,
                },
            ),
        )
        async with api_client_factory(app) as client:
            response = await client.get("/portfolio")
            assert response.status == HTTPStatus.UNAUTHORIZED

    async def test__no_user_id_by_access_token(self) -> None:
        access_token = secrets.token_urlsafe()

        app = Application(
            FakeIdentityProvider(),
            FakePortfolioRepository(),
        )
        async with api_client_factory(app) as client:
            response = await client.get(
                "/portfolio",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.UNAUTHORIZED

    async def test__no_portfolio_by_user_id(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        app = Application(
            FakeIdentityProvider(
                user_id_by_token={
                    access_token: user_id,
                },
            ),
            FakePortfolioRepository(),
        )
        async with api_client_factory(app) as client:
            response = await client.get(
                "/portfolio",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK
            assert await response.json() == {
                "message": "User has no portfolio",
            }


def _make_authorization_header(access_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
    }
