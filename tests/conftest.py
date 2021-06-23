from typing import Final

pytest_plugins: Final = (
    "aiohttp.pytest_plugin",
    "com_redis_test_utils.pytest_plugin",
)
