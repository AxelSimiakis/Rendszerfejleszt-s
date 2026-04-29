from apiflask import HTTPError
from app.blueprints.user import bp
from .schemas import UserRequestSchema, UserResponseSchema, UserLoginSchema
from .service import UserService

@bp.post('/register')
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_register(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 201
    
    raise HTTPError(message=response, status_code=400)

@bp.post('/login')
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    
    raise HTTPError(message=response, status_code=400)