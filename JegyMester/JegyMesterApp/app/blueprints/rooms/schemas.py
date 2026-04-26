from apiflask import Schema
from apiflask.fields import Integer, String

class RoomRequestSchema(Schema):
    name = String(required=True)
    total_capacity = Integer(required=True)

class RoomResponseSchema(Schema):
    id = Integer()
    name = String()
    total_capacity = Integer()