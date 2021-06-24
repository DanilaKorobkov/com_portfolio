from aiohttp import web

from com_portfolio.domain.schemas import PortfolioSchema

from .helpers import get_app
from .responses import make_json_response


def register_views(app: web.Application) -> None:
    app.router.add_get("/portfolios", portfolios_view)
    app.router.add_get("/portfolios/{label}", portfolio_view)


async def portfolios_view(request: web.Request) -> web.Response:
    app = get_app(request.app)
    portfolios = await app.get_portfolios()

    response_body = PortfolioSchema(many=True).dump(portfolios)
    return make_json_response(response_body)


async def portfolio_view(request: web.Request) -> web.Response:
    app = get_app(request.app)

    label = request.match_info["label"]
    portfolio = await app.get_portfolio(label)

    response_body = PortfolioSchema().dump(portfolio)
    return make_json_response(response_body)
