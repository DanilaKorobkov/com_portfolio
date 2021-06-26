import uuid
from typing import Final, Iterator
from uuid import UUID

import pytest

from com_portfolio.context_vars import USER_ID, context_var_set

pytest_plugins: Final = (
    "aiohttp.pytest_plugin",
    "com_redis_test_utils.pytest_plugin",
)


@pytest.fixture
def user_id() -> Iterator[UUID]:
    id_ = uuid.uuid4()
    with context_var_set(USER_ID, id_):
        yield id_
