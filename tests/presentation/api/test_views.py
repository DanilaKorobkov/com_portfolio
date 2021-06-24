import secrets
import uuid
from http import HTTPStatus

from com_portfolio.application import Application
from com_portfolio.domain import PortfolioSchema
from com_portfolio.infrastructure import (
    FakeIdentityProvider,
    FakePortfolioRepository,
)
from com_portfolio.test_utils import PortfolioFactory, api_client_factory


class TestPortfoliosView:

    async def test__hit_many(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        portfolios = PortfolioFactory.build_batch(size=2)
        app = Application(
            FakeIdentityProvider(
                user_id_by_token={
                    access_token: user_id,
                },
            ),
            FakePortfolioRepository(
                user_portfolios={
                    user_id: portfolios,
                },
            ),
        )
        async with api_client_factory(app) as client:
            response = await client.get(
                "/portfolios",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK

            expected = PortfolioSchema(many=True).dump(portfolios)
            assert await response.json() == expected

    async def test__user_has_no_portfolios(self) -> None:
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
                "/portfolios",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK
            assert await response.json() == []


class TestPortfolioView:

    async def test__hit(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        portfolio = PortfolioFactory.build()
        app = Application(
            FakeIdentityProvider(
                user_id_by_token={
                    access_token: user_id,
                },
            ),
            FakePortfolioRepository(
                user_portfolios={
                    user_id: [portfolio],
                },
            ),
        )
        async with api_client_factory(app) as client:
            response = await client.get(
                f"/portfolios/{portfolio.label}",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK
            assert await response.json() == PortfolioSchema().dump(portfolio)

    async def test__missing_authorization_header(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        portfolio = PortfolioFactory.build()
        app = Application(
            FakeIdentityProvider(
                user_id_by_token={
                    access_token: user_id,
                },
            ),
            FakePortfolioRepository(
                user_portfolios={
                    user_id: [portfolio],
                },
            ),
        )

        async with api_client_factory(app) as client:
            response = await client.get(f"/portfolios/{portfolio.label}")
            assert response.status == HTTPStatus.UNAUTHORIZED
            assert await response.json() == {
                "message": "Invalid authorization header",
            }

    async def test__no_user_id_by_access_token(self) -> None:
        access_token = secrets.token_urlsafe()

        app = Application(
            FakeIdentityProvider(),
            FakePortfolioRepository(),
        )

        async with api_client_factory(app) as client:
            response = await client.get(
                "/portfolios/portfolio_label",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.UNAUTHORIZED
            assert await response.json() == {
                "message": "Invalid access token",
            }

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
                "/portfolios/missing_portfolio_label",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK
            assert await response.json() == {
                "message": "Invalid portfolio label",
            }


def _make_authorization_header(access_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
    }
