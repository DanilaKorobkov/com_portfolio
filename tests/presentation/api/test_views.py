import secrets
import uuid
from http import HTTPStatus

from com_portfolio.domain import PortfolioSchema
from com_portfolio.test_utils import (
    PortfolioFactory,
    api_client_factory,
    create_application,
    generate_portfolio_label,
)


class TestPortfoliosView:

    async def test__hit_many(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        user_id_by_token = {
            access_token: user_id,
        }
        portfolios = PortfolioFactory.build_batch(size=2)
        user_portfolios = {
            user_id: portfolios,
        }
        app = create_application(user_portfolios, user_id_by_token)

        async with api_client_factory(app) as client:
            response = await client.get(
                "/portfolios",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK

            schema = PortfolioSchema(many=True, exclude=("id",))
            assert await response.json() == schema.dump(portfolios)

    async def test__user_has_no_portfolios(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        user_id_by_token = {
            access_token: user_id,
        }
        app = create_application(user_id_by_token=user_id_by_token)

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

        user_id_by_token = {
            access_token: user_id,
        }
        portfolio = PortfolioFactory.build()
        user_portfolios = {
            user_id: [portfolio],
        }
        app = create_application(user_portfolios, user_id_by_token)

        async with api_client_factory(app) as client:
            response = await client.get(
                f"/portfolios/{portfolio.label}",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK
            assert await response.json() == (
                PortfolioSchema(exclude=("id",)).dump(portfolio)
            )

    async def test__missing_authorization_header(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        user_id_by_token = {
            access_token: user_id,
        }
        portfolio = PortfolioFactory.build()
        user_portfolios = {
            user_id: [portfolio],
        }
        app = create_application(user_portfolios, user_id_by_token)

        async with api_client_factory(app) as client:
            response = await client.get(f"/portfolios/{portfolio.label}")
            assert response.status == HTTPStatus.UNAUTHORIZED
            assert await response.json() == {
                "message": "Invalid authorization header",
            }

    async def test__no_user_id_by_access_token(self) -> None:
        access_token = secrets.token_urlsafe()

        app = create_application()

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

        user_id_by_token = {
            access_token: user_id,
        }
        app = create_application(user_id_by_token=user_id_by_token)

        async with api_client_factory(app) as client:
            response = await client.get(
                "/portfolios/missing_portfolio_label",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.BAD_REQUEST
            assert await response.json() == {
                "message": "Missing portfolio",
            }


class TestCreateNewPortfolioView:

    async def test__portfolio_with_label_is_not_exists(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()
        label = generate_portfolio_label()

        user_id_by_token = {
            access_token: user_id,
        }
        app = create_application(user_id_by_token=user_id_by_token)

        async with api_client_factory(app) as client:
            response = await client.post(
                f"/portfolios/{label}",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK
            assert await response.json() == {
                "message": "OK",
            }
            response = await client.get(
                f"/portfolios/{label}",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.OK

    async def test__portfolio_with_label_exists(self) -> None:
        user_id = uuid.uuid4()
        access_token = secrets.token_urlsafe()

        portfolio = PortfolioFactory.build()
        user_portfolios = {
            user_id: [portfolio],
        }
        user_id_by_token = {
            access_token: user_id,
        }
        app = create_application(user_portfolios, user_id_by_token)

        async with api_client_factory(app) as client:
            response = await client.post(
                f"/portfolios/{portfolio.label}",
                headers=_make_authorization_header(access_token),
            )
            assert response.status == HTTPStatus.BAD_REQUEST
            assert await response.json() == {
                "message": "Portfolio already exists",
            }


def _make_authorization_header(access_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
    }
