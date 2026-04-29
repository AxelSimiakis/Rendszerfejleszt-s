from apiflask import APIBlueprint, HTTPError
from .service import TicketService
from .schemas import TicketRequestSchema, TicketResponseSchema
from app.blueprints.tickets import bp

@bp.get('/')
@bp.output(TicketResponseSchema(many=True))
def get_tickets():
    """Osszes eladott jegy listazasa"""
    return TicketService.get_all_tickets()

@bp.post('/')
@bp.input(TicketRequestSchema, location="json")
@bp.output(TicketResponseSchema)
def add_ticket(json_data):
    """Uj jegy vasarlasa / kiallitasa"""
    success, response = TicketService.create_ticket(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:ticket_id>')
def delete_ticket(ticket_id):
    """Jegy visszavaltasa (torlese) ID alapjan"""
    success, response = TicketService.delete_ticket(ticket_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)