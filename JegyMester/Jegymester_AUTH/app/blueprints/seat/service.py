from app.extensions import db
from app.models.seat import Seat
from app.models.screening import Screening
from app.models.ticket import Ticket
from sqlalchemy import select
from .schemas import SeatResponseSchema, ScreeningSeatResponseSchema
import traceback

class SeatService:
    @staticmethod
    def get_all_seats():
        try:
            seats = db.session.execute(select(Seat).order_by(Seat.room_id, Seat.row_num, Seat.seat_num)).scalars().all()
            return SeatResponseSchema(many=True).dump(seats)
        except Exception as ex:
            print(f"Hiba a szekek lekerdezesenel: {ex}")
            return []

    @staticmethod
    def get_seats_for_screening(screening_id):
        screening = db.session.get(Screening, screening_id)
        if not screening:
            return False, "Vetites nem talalhato"

        seats = db.session.execute(
            select(Seat).where(Seat.room_id == screening.room_id).order_by(Seat.row_num, Seat.seat_num)
        ).scalars().all()

        reserved_ids = set(db.session.execute(
            select(Ticket.seat_id).where(
                Ticket.screening_id == screening_id,
                Ticket.status == 'valid'
            )
        ).scalars().all())

        result = []
        for seat in seats:
            row_letter = chr(ord('A') + int(seat.row_num) - 1) if seat.row_num else ''
            result.append({
                'id': seat.id,
                'room_id': seat.room_id,
                'row_num': seat.row_num,
                'seat_num': seat.seat_num,
                'reserved': seat.id in reserved_ids,
                'label': f'{row_letter}{seat.seat_num}',
            })
        return True, ScreeningSeatResponseSchema(many=True).dump(result)

    @staticmethod
    def create_seat(data):
        try:
            seat = Seat(**data)
            db.session.add(seat)
            db.session.commit()
            return True, SeatResponseSchema().dump(seat)
        except Exception as ex:
            db.session.rollback()
            print("HIBA A SZEK MENTESENEL:")
            traceback.print_exc()
            return False, str(ex)

    @staticmethod
    def delete_seat(seat_id):
        try:
            seat = db.session.get(Seat, seat_id)
            if not seat:
                return False, "Szek nem talalhato"
            db.session.delete(seat)
            db.session.commit()
            return True, "Szek sikeresen torolve"
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)
