from apiflask import APIBlueprint, HTTPError
from .service import RoleService
from .schemas import RoleRequestSchema, RoleResponseSchema
from app.extensions import auth

bp = APIBlueprint('role', __name__, tag='role')

@bp.get('/')
@bp.output(RoleResponseSchema(many=True))
@bp.auth_required(auth)
def get_roles():
    """Osszes szerepkor listazasa"""
    return RoleService.get_all_roles()

@bp.post('/')
@bp.input(RoleRequestSchema, location="json")
@bp.output(RoleResponseSchema)
@bp.auth_required(auth)
def add_role(json_data):
    """Uj szerepkor (pl. Admin, Cashier) letrehozasa"""
    success, response = RoleService.create_role(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:role_id>')
@bp.auth_required(auth)
def delete_role(role_id):
    """Szerepkor torlese ID alapjan"""
    success, response = RoleService.delete_role(role_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)