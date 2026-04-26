from apiflask import Schema
from apiflask.fields import Integer, String

class ScreeningRequestSchema(Schema):
    movie_id = Integer(required=True)
    room_id = Integer(required=True)
   
    start_time = String(required=True) 

class ScreeningResponseSchema(Schema):
    id = Integer()
    movie_id = Integer()
    room_id = Integer()
    
    start_time = String()