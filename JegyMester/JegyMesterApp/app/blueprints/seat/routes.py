from apiflask import APIBlueprint, HTTPError
from .service import SeatService
from .schemas import SeatRequestSchema, SeatResponseSchema
from app.extensions import auth

bp = APIBlueprint('seat', __name__, tag='seat')

@bp.get('/')
@bp.output(SeatResponseSchema(many=True))
@bp.auth_required(auth)
def get_seats():
    """Osszes szek listazasa"""
    return SeatService.get_all_seats()

@bp.post('/')
@bp.input(SeatRequestSchema, location="json")
@bp.output(SeatResponseSchema)
@bp.auth_required(auth)
def add_seat(json_data):
    """Uj szek hozzaadasa egy teremhez"""
    success, response = SeatService.create_seat(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:seat_id>')
@bp.auth_required(auth)
def delete_seat(seat_id):
    """Szek torlese ID alapjan"""
    success, response = SeatService.delete_seat(seat_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)