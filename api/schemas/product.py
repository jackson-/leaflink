from marshmallow import fields

from base import BaseSchema
from company_raw import CompanyRawSchema


class ProductSchema(BaseSchema):
    # Keys
    id = fields.Int()

    # Own properties
    name = fields.String()
    description = fields.String()
    company_type = fields.String()
    price = fields.Float()

    # Relationships
    company = fields.Nested(CompanyRawSchema)