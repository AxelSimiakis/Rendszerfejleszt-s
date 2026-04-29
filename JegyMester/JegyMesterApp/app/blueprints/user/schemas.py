from apiflask import Schema
from apiflask.fields import String, Email, Integer

class UserRequestSchema(Schema):
    name = String()
    email = Email(required=True)
    password = String(required=True)
    phone_number = String(required=True)

class UserResponseSchema(Schema):
    id = Integer()
    name = String()
    email = String()

class UserLoginSchema(Schema):
    email = Email(required=True)
    password = String(required=True)