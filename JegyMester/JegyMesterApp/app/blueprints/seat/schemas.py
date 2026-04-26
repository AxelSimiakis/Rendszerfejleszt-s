from apiflask import Schema
from apiflask.fields import Integer

class SeatRequestSchema(Schema):
    room_id = Integer(required=True)
    row_num = Integer(required=True)
    seat_num = Integer(required=True)

class SeatResponseSchema(Schema):
    id = Integer()
    room_id = Integer()
    row_num = Integer()
    seat_num = Integer()