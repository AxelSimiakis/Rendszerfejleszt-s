from apiflask import APIBlueprint, HTTPError
from .service import TicketService
from .schemas import TicketRequestSchema, TicketResponseSchema, ReserveTicketsRequestSchema, ReserveTicketsResponseSchema
from app.extensions import auth

bp = APIBlueprint('ticket', __name__, tag='ticket')

@bp.get('/')
@bp.output(TicketResponseSchema(many=True))
def get_tickets():
    return TicketService.get_all_tickets()

@bp.post('/')
@bp.auth_required(auth)
@bp.input(TicketRequestSchema, location="json")
@bp.output(TicketResponseSchema)
def add_ticket(json_data):
    success, response = TicketService.create_ticket(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.post('/reserve')
@bp.input(ReserveTicketsRequestSchema, location="json")
@bp.output(ReserveTicketsResponseSchema)
@bp.auth_required(auth)
def reserve_tickets(json_data):
    current_user_id = auth.current_user.get('user_id')
    success, response = TicketService.reserve_tickets(json_data, current_user_id)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:ticket_id>')
@bp.auth_required(auth)
def delete_ticket(ticket_id):
    success, response = TicketService.delete_ticket(ticket_id)
    if success:
        return '', 204
    raise HTTPError(message=response, status_code=404)
