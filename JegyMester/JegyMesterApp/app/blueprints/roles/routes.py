from apiflask import APIBlueprint, HTTPError
from .service import RoleService
from .schemas import RoleRequestSchema, RoleResponseSchema
from app.blueprints.roles import bp

@bp.get('/')
@bp.output(RoleResponseSchema(many=True))
def get_roles():
    """Osszes szerepkor listazasa"""
    return RoleService.get_all_roles()

@bp.post('/')
@bp.input(RoleRequestSchema, location="json")
@bp.output(RoleResponseSchema)
def add_role(json_data):
    """Uj szerepkor (pl. Admin, Cashier) letrehozasa"""
    success, response = RoleService.create_role(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:role_id>')
def delete_role(role_id):
    """Szerepkor torlese ID alapjan"""
    success, response = RoleService.delete_role(role_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)