from apiflask import Schema
from apiflask.fields import Integer, String, Float

class TransactionRequestSchema(Schema):
    user_id = Integer(required=True)
    total_amount = Float(required=True)
    payment_method = String(required=True)
    status = String(load_default="success")

class TransactionResponseSchema(Schema):
    id = Integer()
    user_id = Integer()
    purchase_time = String() 
    total_amount = Float()
    payment_method = String()
    status = String()