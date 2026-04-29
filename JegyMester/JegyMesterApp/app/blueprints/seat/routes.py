from apiflask import APIBlueprint, HTTPError
from .service import SeatService
from .schemas import SeatRequestSchema, SeatResponseSchema
from app.blueprints.seat import bp

@bp.get('/')
@bp.output(SeatResponseSchema(many=True))
def get_seats():
    """Osszes szek listazasa"""
    return SeatService.get_all_seats()

@bp.post('/')
@bp.input(SeatRequestSchema, location="json")
@bp.output(SeatResponseSchema)
def add_seat(json_data):
    """Uj szek hozzaadasa egy teremhez"""
    success, response = SeatService.create_seat(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:seat_id>')
def delete_seat(seat_id):
    """Szek torlese ID alapjan"""
    success, response = SeatService.delete_seat(seat_id)
    if success:
        return {'message': response}, 204
    if response == "Szek nem talalhato":
        raise HTTPError(message=response, status_code=404)
    if "nem torolheto" in response:
        raise HTTPError(message=response, status_code=409)
    raise HTTPError(message=response, status_code=400)