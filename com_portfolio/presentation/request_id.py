from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, Optional
from uuid import UUID


def get_request_id() -> Optional[UUID]:
    try:
        return _REQUEST_ID.get()
    except LookupError:
        return None


@contextmanager
def request_id_set(value: UUID) -> Iterator[None]:
    token = _REQUEST_ID.set(value)
    try:
        yield
    finally:
        _REQUEST_ID.reset(token)


_REQUEST_ID: ContextVar[UUID] = ContextVar("REQUEST_ID")
