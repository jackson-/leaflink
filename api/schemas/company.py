from marshmallow import fields

from .base import BaseSchema
from .product_raw import ProductRawSchema

class CompanySchema(BaseSchema):
    # Keys
    id = fields.Int()

    # Own properties
    name = fields.String()
    description = fields.String()
    company_type = fields.String()

    # Reltionships
    products = fields.Nested(
        ProductRawSchema,
        many=True,
    )