from apiflask import Schema
from apiflask.fields import Integer, String, List

class TicketRequestSchema(Schema):
    transaction_id = Integer(required=True)
    screening_id = Integer(required=True)
    seat_id = Integer(required=True)
    issued_by_id = Integer(load_default=None)
    status = String(load_default="valid")

class TicketResponseSchema(Schema):
    id = Integer()
    transaction_id = Integer()
    screening_id = Integer()
    seat_id = Integer()
    issued_by_id = Integer()
    status = String()

class ReserveTicketsRequestSchema(Schema):
    screening_id = Integer(required=True)
    seat_ids = List(Integer(), required=True)

class ReserveTicketsResponseSchema(Schema):
    transaction_id = Integer()
    ticket_ids = List(Integer())
    status = String()
