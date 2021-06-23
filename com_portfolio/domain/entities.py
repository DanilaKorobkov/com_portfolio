from uuid import UUID

import attr


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Entity:
    id: UUID


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Portfolio(Entity):
    label: str
    positions: tuple["Position"] = attr.ib(converter=tuple)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Position:
    company: "Company"
    count: int
    average_price: float


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Company:
    ticker: str
