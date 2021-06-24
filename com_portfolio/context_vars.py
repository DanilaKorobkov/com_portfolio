from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, TypeVar
from uuid import UUID

USER_ID: ContextVar[UUID] = ContextVar("USER_ID")
REQUEST_ID: ContextVar[UUID] = ContextVar("REQUEST_ID")

_T = TypeVar("_T")


@contextmanager
def context_var_set(var: ContextVar[_T], value: _T) -> Iterator[None]:
    token = var.set(value)
    try:
        yield
    finally:
        var.reset(token)
