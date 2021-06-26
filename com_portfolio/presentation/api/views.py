from aiohttp import web

from com_portfolio.domain.schemas import PortfolioSchema

from .exceptions import InvalidAuthorizationHeader
from .helpers import get_app
from .responses import make_json_response


def register_views(app: web.Application) -> None:
    app.router.add_get("/portfolios", portfolios_view)
    app.router.add_get("/portfolios/{label}", portfolio_view)
    app.router.add_post("/portfolios/{label}", create_new_portfolio_view)


async def portfolios_view(request: web.Request) -> web.Response:
    access_token = _get_access_token(request)

    app = get_app(request.app)
    portfolios = await app.get_portfolios(access_token)

    schema = PortfolioSchema(many=True, exclude=("id",))
    response_body = schema.dump(portfolios)
    return make_json_response(response_body)


async def portfolio_view(request: web.Request) -> web.Response:
    access_token = _get_access_token(request)
    label = request.match_info["label"]

    app = get_app(request.app)
    portfolio = await app.get_portfolio(access_token, label)

    schema = PortfolioSchema(exclude=("id",))
    response_body = schema.dump(portfolio)
    return make_json_response(response_body)


async def create_new_portfolio_view(request: web.Request) -> web.Response:
    access_token = _get_access_token(request)
    label = request.match_info["label"]

    app = get_app(request.app)
    await app.create_portfolio(access_token, label)

    response_body = {
        "message": "OK",
    }
    return make_json_response(response_body)


def _get_access_token(request: web.Request) -> str:
    try:
        _, token = request.headers['Authorization'].strip().split()
    except (KeyError, ValueError) as e:
        raise InvalidAuthorizationHeader from e
    else:
        return token
