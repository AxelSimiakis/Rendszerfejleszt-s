from app.extensions import db
from app.models.screening import Screening
from sqlalchemy import select
from .schemas import ScreeningResponseSchema
from datetime import datetime
import traceback

class ScreeningService:
    @staticmethod
    def get_all_screenings():
        try:
            screenings = db.session.execute(select(Screening)).scalars().all()
            return ScreeningResponseSchema(many=True).dump(screenings)
        except Exception as ex:
            print(f"Hiba a vetitesek lekerdezesenel: {ex}")
            return []

    @staticmethod
    def create_screening(data):
        try:
            
            start_time_str = data.get('start_time')
            
           
            if start_time_str:
                 data['start_time'] = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')

            screening = Screening(**data)
            db.session.add(screening)
            db.session.commit()
            return True, ScreeningResponseSchema().dump(screening)
        except Exception as ex:
            db.session.rollback()
            print("HIBA A VETITES MENTESENEL:")
            traceback.print_exc()
            return False, str(ex)

    @staticmethod
    def delete_screening(screening_id):
        try:
            screening = db.session.get(Screening, screening_id)
            if not screening:
                return False, "Vetites nem talalhato"
            db.session.delete(screening)
            db.session.commit()
            return True, "Vetites sikeresen torolve"
        except Exception as ex:
            db.session.rollback()
            print(f"Torlesi hiba: {ex}")
            return False, str(ex)