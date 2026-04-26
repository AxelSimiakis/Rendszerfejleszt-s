from apiflask import APIBlueprint, HTTPError
from .service import TicketService
from .schemas import TicketRequestSchema, TicketResponseSchema
from app.extensions import auth

bp = APIBlueprint('ticket', __name__, tag='ticket')

@bp.get('/')
@bp.output(TicketResponseSchema(many=True))
@bp.auth_required(auth)
def get_tickets():
    """Osszes eladott jegy listazasa"""
    return TicketService.get_all_tickets()

@bp.post('/')
@bp.input(TicketRequestSchema, location="json")
@bp.output(TicketResponseSchema)
@bp.auth_required(auth)
def add_ticket(json_data):
    """Uj jegy vasarlasa / kiallitasa"""
    success, response = TicketService.create_ticket(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:ticket_id>')
@bp.auth_required(auth)
def delete_ticket(ticket_id):
    """Jegy visszavaltasa (torlese) ID alapjan"""
    success, response = TicketService.delete_ticket(ticket_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)