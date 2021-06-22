from aiohttp import web

from .helpers import get_app
from .responses import make_json_response


def register_views(app: web.Application) -> None:
    app.router.add_get("/portfolio", portfolio_view)


async def portfolio_view(request: web.Request) -> web.Response:
    app = get_app(request.app)

    access_token = _get_access_token(request)
    portfolio = await app.get_portfolio(access_token)

    response_body = {
        "portfolio": {
            "id": str(portfolio.id),
            "user_id": str(portfolio.user_id),
        },
    }
    return make_json_response(response_body)


def _get_access_token(request: web.Request) -> str:
    try:
        _, token = request.headers['Authorization'].strip().split()
    except (KeyError, ValueError) as e:
        raise web.HTTPUnauthorized from e
    else:
        return token
