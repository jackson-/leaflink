from marshmallow import fields

from base import BaseSchema
from product_raw import ProductRawSchema

class OrderRawSchema(BaseSchema):
    # Keys
    id = fields.Int()

    # Own properties
    name = fields.String()
    description = fields.String()
    price = fields.Float()

    # Relationships
    # products = fields.Nested(
    #     ProductRawSchema,
    #     many=True,
    # )