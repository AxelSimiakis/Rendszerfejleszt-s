from app.extensions import db
from app.models.transaction import Transaction
from sqlalchemy import select
from .schemas import TransactionResponseSchema
import traceback

class TransactionService:
    @staticmethod
    def get_all_transactions():
        try:
            transactions = db.session.execute(select(Transaction)).scalars().all()
            
            result = []
            for t in transactions:
                t_dict = {
                    "id": t.id,
                    "user_id": t.user_id,
                    "purchase_time": t.purchase_time.isoformat() if t.purchase_time else None,
                    "total_amount": t.total_amount,
                    "payment_method": t.payment_method,
                    "status": t.status
                }
                result.append(t_dict)
            return TransactionResponseSchema(many=True).dump(result)
        except Exception as ex:
            print(f"Hiba a tranzakciok lekerdezesenel: {ex}")
            return []

    @staticmethod
    def create_transaction(data):
        try:
           
            transaction = Transaction(**data)
            db.session.add(transaction)
            db.session.commit()
            
           
            response_data = {
                 "id": transaction.id,
                 "user_id": transaction.user_id,
                 "purchase_time": transaction.purchase_time.isoformat() if transaction.purchase_time else None,
                 "total_amount": transaction.total_amount,
                 "payment_method": transaction.payment_method,
                 "status": transaction.status
            }
            return True, TransactionResponseSchema().dump(response_data)
        except Exception as ex:
            db.session.rollback()
            print("HIBA A TRANZAKCIO MENTESENEL:")
            traceback.print_exc()
            return False, str(ex)

    @staticmethod
    def delete_transaction(transaction_id):
        try:
            transaction = db.session.get(Transaction, transaction_id)
            if not transaction:
                return False, "Tranzakcio nem talalhato"
            db.session.delete(transaction)
            db.session.commit()
            return True, "Tranzakcio sikeresen torolve"
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)