from app.extensions import db
from app.models.seat import Seat
from sqlalchemy import select
from .schemas import SeatResponseSchema
import traceback

class SeatService:
    @staticmethod
    def get_all_seats():
        try:
            seats = db.session.execute(select(Seat)).scalars().all()
            return SeatResponseSchema(many=True).dump(seats)
        except Exception as ex:
            print(f"Hiba a szekek lekerdezesenel: {ex}")
            return []

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