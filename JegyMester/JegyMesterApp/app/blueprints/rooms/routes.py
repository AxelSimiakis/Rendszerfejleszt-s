from apiflask import APIBlueprint, HTTPError
from .service import RoomService
from .schemas import RoomRequestSchema, RoomResponseSchema
from app.extensions import auth

bp = APIBlueprint('room', __name__, tag='room')

@bp.get('/')
@bp.output(RoomResponseSchema(many=True))
@bp.auth_required(auth)
def get_rooms():
    """Osszes terem listazasa"""
    return RoomService.get_all_rooms()

@bp.post('/')
@bp.input(RoomRequestSchema, location="json")
@bp.output(RoomResponseSchema)
@bp.auth_required(auth)
def add_room(json_data):
    """Uj terem felvetele"""
    success, response = RoomService.create_room(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:room_id>')
@bp.auth_required(auth)
def delete_room(room_id):
    """Terem torlese ID alapjan"""
    success, response = RoomService.delete_room(room_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)