from marshmallow import fields

from base import BaseSchema
from product_raw import ProductRawSchema

class LineItemSchema(BaseSchema):
  # Keys
  id = fields.Int()

  # Own properties
  quantity = fields.Int()
  unit_price = fields.Float()

  # Relationships
  product = fields.Nested(
      ProductRawSchema,
  )