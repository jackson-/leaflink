from marshmallow import fields

from base import BaseSchema

class CompanyRawSchema(BaseSchema):
    # Keys
    id = fields.Int()

    # Own properties
    name = fields.String()
    description = fields.String()
    company_type = fields.String()