from apiflask import APIBlueprint, HTTPError
from .service import ScreeningService
from .schemas import ScreeningRequestSchema, ScreeningResponseSchema
from app.blueprints.screenings import bp

@bp.get('/')
@bp.output(ScreeningResponseSchema(many=True))
def get_screenings():
    """Osszes vetites lekerese"""
    return ScreeningService.get_all_screenings()

@bp.post('/')
@bp.input(ScreeningRequestSchema, location="json")
@bp.output(ScreeningResponseSchema)
def add_screening(json_data):
    """Uj vetites felvetele"""
    success, response = ScreeningService.create_screening(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:screening_id>')
def delete_screening(screening_id):
    """Vetites torlese ID alapjan"""
    success, response = ScreeningService.delete_screening(screening_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)