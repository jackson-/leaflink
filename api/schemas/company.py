from marshmallow import fields

from base import BaseSchema

class CompanySchema(BaseSchema):
    # Keys
    id = fields.Int()

    # Own properties
    name = fields.String()
    description = fields.String()