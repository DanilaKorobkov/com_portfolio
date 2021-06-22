from uuid import UUID

import attr


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Entity:
    id: UUID


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Portfolio(Entity):
    user_id: UUID
