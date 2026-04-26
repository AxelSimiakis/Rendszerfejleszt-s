from app.extensions import db
from app.models.room import Room
from sqlalchemy import select
from .schemas import RoomResponseSchema

class RoomService:
    @staticmethod
    def get_all_rooms():
        try:
            rooms = db.session.execute(select(Room)).scalars().all()
            return RoomResponseSchema(many=True).dump(rooms)
        except Exception as ex:
            print(f"Hiba a termek lekerdezesenel: {ex}")
            return []

    @staticmethod
    def create_room(data):
        try:
            room = Room(**data)
            db.session.add(room)
            db.session.commit()
            return True, RoomResponseSchema().dump(room)
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)

    @staticmethod
    def delete_room(room_id):
        try:
            room = db.session.get(Room, room_id)
            if not room:
                return False, "Terem nem talalhato"
            
            if room.seats:
                return False, f"Terem nem torolheto, mert {len(room.seats)} szek van hozzarendelve"

            if room.screenings:
                return False, f"Terem nem torolheto, mert {len(room.screenings)} vetites van beutemezve"
            
            db.session.delete(room)
            db.session.commit()
            return True, "Terem sikeresen torolve"
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)