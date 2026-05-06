from app.extensions import db
from app.models.ticket import Ticket
from app.models.seat import Seat
from app.models.screening import Screening
from app.models.transaction import Transaction
from sqlalchemy import select
from .schemas import TicketResponseSchema, ReserveTicketsResponseSchema
from decimal import Decimal
import traceback

TICKET_PRICE = Decimal('2500.00')

class TicketService:
    @staticmethod
    def get_all_tickets():
        try:
            tickets = db.session.execute(select(Ticket)).scalars().all()
            return TicketResponseSchema(many=True).dump(tickets)
        except Exception as ex:
            print(f"Hiba a jegyek lekerdezesenel: {ex}")
            return []

    @staticmethod
    def create_ticket(data):
        try:
            ok, message = TicketService._validate_ticket(data.get('screening_id'), data.get('seat_id'))
            if not ok:
                return False, message

            ticket = Ticket(**data)
            db.session.add(ticket)
            db.session.commit()
            return True, TicketResponseSchema().dump(ticket)
        except Exception as ex:
            db.session.rollback()
            print("HIBA A JEGY MENTESENEL:")
            traceback.print_exc()
            return False, str(ex)

    @staticmethod
    def reserve_tickets(data, user_id):
        try:
            screening_id = data.get('screening_id')
            seat_ids = data.get('seat_ids') or []
            if not seat_ids:
                return False, "Nincs kivalasztott szek"

            # Duplikált szék azonosító kiszűrése úgy, hogy a sorrend megmaradjon.
            seat_ids = list(dict.fromkeys(seat_ids))

            for seat_id in seat_ids:
                ok, message = TicketService._validate_ticket(screening_id, seat_id)
                if not ok:
                    return False, message

            transaction = Transaction(
                user_id=user_id,
                total_amount=TICKET_PRICE * len(seat_ids),
                payment_method='online',
                status='success',
            )
            db.session.add(transaction)
            db.session.flush()

            tickets = []
            for seat_id in seat_ids:
                ticket = Ticket(
                    transaction_id=transaction.id,
                    screening_id=screening_id,
                    seat_id=seat_id,
                    issued_by_id=user_id,
                    status='valid',
                )
                db.session.add(ticket)
                tickets.append(ticket)

            db.session.commit()
            response = {
                'transaction_id': transaction.id,
                'ticket_ids': [ticket.id for ticket in tickets],
                'status': 'success',
            }
            return True, ReserveTicketsResponseSchema().dump(response)
        except Exception as ex:
            db.session.rollback()
            print("HIBA A FOGLALASNAL:")
            traceback.print_exc()
            return False, str(ex)

    @staticmethod
    def _validate_ticket(screening_id, seat_id):
        seat = db.session.get(Seat, seat_id)
        if not seat:
            return False, "Hiba: A megadott szek nem letezik!"

        screening = db.session.get(Screening, screening_id)
        if not screening:
            return False, "Hiba: A megadott vetites nem letezik!"

        if seat.room_id != screening.room_id:
            return False, "Hiba: Ez a szek nem abban a teremben van, ahol a vetites!"

        existing_ticket = db.session.execute(
            select(Ticket).where(
                Ticket.screening_id == screening_id,
                Ticket.seat_id == seat_id,
                Ticket.status == 'valid'
            )
        ).scalar_one_or_none()

        if existing_ticket:
            return False, "Hiba: Ez a szek mar foglalt erre a vetitesre!"

        return True, None

    @staticmethod
    def delete_ticket(ticket_id):
        try:
            ticket = db.session.get(Ticket, ticket_id)
            if not ticket:
                return False, "Jegy nem talalhato"
            db.session.delete(ticket)
            db.session.commit()
            return True, "Jegy sikeresen torolve"
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)
