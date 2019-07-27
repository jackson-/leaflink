from marshmallow import fields

from base import BaseSchema

class ProductRawSchema(BaseSchema):
    # Keys
    id = fields.Int()

    # Own properties
    name = fields.String()
    description = fields.String()
    price = fields.Float()
