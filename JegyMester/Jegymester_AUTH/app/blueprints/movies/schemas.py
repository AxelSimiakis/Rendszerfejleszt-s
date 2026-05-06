from apiflask import Schema
from apiflask.fields import String, Integer

class MovieRequestSchema(Schema):
    title = String(required=True)
    description = String()
    duration_minutes = Integer()

class MovieResponseSchema(Schema):
    id = Integer()
    title = String()
    description = String()
    duration_minutes = Integer()