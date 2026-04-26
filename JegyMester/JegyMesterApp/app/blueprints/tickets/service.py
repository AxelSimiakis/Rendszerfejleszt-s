from app.extensions import db
from app.models.ticket import Ticket
from app.models.seat import Seat
from app.models.screening import Screening
from sqlalchemy import select
from .schemas import TicketResponseSchema
import traceback

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
            screening_id = data.get('screening_id')
            seat_id = data.get('seat_id')

            seat = db.session.get(Seat, seat_id)
            if not seat:
                return False, "Hiba: A megadott szek nem letezik (tulfoglalas elleni vedelem)!"

            
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