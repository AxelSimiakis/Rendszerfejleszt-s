from apiflask import APIBlueprint, HTTPError
from .service import SeatService
from .schemas import SeatRequestSchema, SeatResponseSchema, ScreeningSeatResponseSchema
from app.extensions import auth

bp = APIBlueprint('seat', __name__, tag='seat')

@bp.get('/')
@bp.output(SeatResponseSchema(many=True))
def get_seats():
    return SeatService.get_all_seats()

@bp.get('/<int:screening_id>')
@bp.output(ScreeningSeatResponseSchema(many=True))
def get_seats_for_screening(screening_id):
    success, response = SeatService.get_seats_for_screening(screening_id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=404)

@bp.post('/')
@bp.input(SeatRequestSchema, location="json")
@bp.output(SeatResponseSchema)
def add_seat(json_data):
    success, response = SeatService.create_seat(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:seat_id>')
@bp.auth_required(auth)
def delete_seat(seat_id):
    success, response = SeatService.delete_seat(seat_id)
    if success:
        return '', 204
    raise HTTPError(message=response, status_code=404)
