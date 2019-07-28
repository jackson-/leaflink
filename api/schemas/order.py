from marshmallow import fields

from .base import BaseSchema
from .line_item import LineItemSchema
from .company_raw import CompanyRawSchema

class OrderSchema(BaseSchema):
    # Keys
    id = fields.Int()

    # Own properties
    total = fields.Int()

    # Reltionships
    line_items = fields.Nested(
        LineItemSchema,
        many=True
    )
    buyer = fields.Nested(
      CompanyRawSchema
    )
    seller = fields.Nested(
      CompanyRawSchema
    )