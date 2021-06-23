import aioredis
from aiohttp import web
from environs import Env

from com_portfolio.application import Application
from com_portfolio.infrastructure import (
    FakeIdentityProvider,
    RedisPortfolioRepository,
)
from com_portfolio.presentation import api


def main() -> None:
    web.run_app(create_app(), port=8081)


async def create_app() -> web.Application:
    env = Env()

    redis_client = await aioredis.create_redis_pool(
        env("REDIS_URL", ""),
        minsize=env.int("REDIS_POOL_MIN_SIZE", "0"),
        maxsize=env.int("REDIS_POOL_MAX_SIZE", "5"),
    )

    app = Application(
        FakeIdentityProvider(),
        RedisPortfolioRepository(redis_client),
    )
    web_app = api.create_web_app(app)

    async def _close_redis_client(_: web.Application) -> None:
        redis_client.close()
        await redis_client.wait_closed()

    web_app.on_cleanup.append(_close_redis_client)
    return web_app


if __name__ == "__main__":
    main()
