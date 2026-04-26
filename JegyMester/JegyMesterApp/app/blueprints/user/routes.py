from apiflask import HTTPError
from . import bp
from .schemas import UserRequestSchema, UserResponseSchema, UserLoginSchema
from .schemas import RoleSchema 
from .service import UserService
from app.extensions import auth
from app.blueprints import role_required

@bp.route('/')
def index():
    return 'This is The User Blueprint'

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


@bp.get('/myroles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth) # <--- APIFlask token ellenorzes
def user_list_user_roles():
    current_user_id = auth.current_user.get("user_id")
    
    success, response = UserService.list_user_roles(current_user_id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/roles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth) # <--- APIFlask token ellenorzes (Bejelentkezes kotelezo)
@role_required(["User"]) # <--- Sajat RBAC: Csak "User" role-lal engedjuk be!
def user_list_roles():
    success, response = UserService.user_list_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)