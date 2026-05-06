from apiflask import Schema
from apiflask.fields import Integer, String

class RoleRequestSchema(Schema):
    name = String(required=True)

class RoleResponseSchema(Schema):
    id = Integer()
    name = String()