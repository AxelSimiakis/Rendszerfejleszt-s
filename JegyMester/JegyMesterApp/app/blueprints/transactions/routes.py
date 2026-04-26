from apiflask import APIBlueprint, HTTPError
from .service import TransactionService
from .schemas import TransactionRequestSchema, TransactionResponseSchema
from app.extensions import auth

bp = APIBlueprint('transaction', __name__, tag='transaction')

@bp.get('/')
@bp.output(TransactionResponseSchema(many=True))
@bp.auth_required(auth)
def get_transactions():
    """Osszes tranzakcio listazasa"""
    return TransactionService.get_all_transactions()

@bp.post('/')
@bp.input(TransactionRequestSchema, location="json")
@bp.output(TransactionResponseSchema)
@bp.auth_required(auth)
def add_transaction(json_data):
    """Uj tranzakcio letrehozasa (fizetes)"""
    success, response = TransactionService.create_transaction(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:transaction_id>')
@bp.auth_required(auth)
def delete_transaction(transaction_id):
    """Tranzakcio torlese (visszaterites szimulalasa)"""
    success, response = TransactionService.delete_transaction(transaction_id)
    if success:
        return {'message': response}, 204
    raise HTTPError(message=response, status_code=404)