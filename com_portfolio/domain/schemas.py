from typing import Generic, Type, TypeVar

from marshmallow import Schema, fields, post_load

from .entities import Company, Portfolio, Position

_T = TypeVar("_T")


class EntitySchema(Generic[_T], Schema):
    __model__: Type[_T]

    @post_load
    def release(self, data: dict, **_) -> _T:
        return self.__model__(**data)  # type: ignore


class CompanySchema(EntitySchema):
    __model__ = Company

    ticker = fields.Str(required=True)


class PositionSchema(EntitySchema):
    __model__ = Position

    company = fields.Nested(CompanySchema, required=True)
    count = fields.Int(required=True)
    average_price = fields.Float(required=True)


class PortfolioSchema(EntitySchema):
    __model__ = Portfolio

    id = fields.UUID(required=True)
    label = fields.Str(required=True)
    positions = fields.List(fields.Nested(PositionSchema), required=True)
