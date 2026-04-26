from apiflask import Schema
from apiflask.fields import String, Email, Integer, List, Nested

class RoleSchema(Schema):
    id = Integer()
    name = String()

class UserRequestSchema(Schema):
    name = String()
    email = Email(required=True)
    password = String(required=True)
    phone_number = String(required=True)

class UserResponseSchema(Schema):
    id = Integer()
    name = String()
    email = String()
    token = String() 

class UserLoginSchema(Schema):
    email = Email(required=True)
    password = String(required=True)

class PayloadSchema(Schema):
    user_id = Integer() 
    roles = List(Nested(RoleSchema)) 
    exp = Integer()