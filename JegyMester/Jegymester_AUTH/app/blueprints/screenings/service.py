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
            start_time_str = data.get("start_time")

            if start_time_str:
                data["start_time"] = ScreeningService.parse_datetime(start_time_str)

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
    def update_screening(screening_id, data):
        try:
            screening = db.session.get(Screening, screening_id)

            if not screening:
                return False, "Vetites nem talalhato"

            start_time_str = data.get("start_time")

            if start_time_str:
                data["start_time"] = ScreeningService.parse_datetime(start_time_str)

            for key, value in data.items():
                setattr(screening, key, value)

            db.session.commit()

            return True, ScreeningResponseSchema().dump(screening)

        except Exception as ex:
            db.session.rollback()
            print("HIBA A VETITES MODOSITASANAL:")
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

    @staticmethod
    def parse_datetime(value):
        """
        Elfogadott formátumok például:
        - 2026-05-06T15:30
        - 2026-05-06T15:30:00
        - 2026-05-06T15:30:00.000Z
        - 2026-05-06T15:30:00.000+00:00
        """

        if isinstance(value, datetime):
            return value

        if not isinstance(value, str):
            raise ValueError("A start_time nem megfelelo formatumu")

        value = value.strip()

        if value.endswith("Z"):
            value = value[:-1]

        if "." in value:
            value = value.split(".")[0]

        return datetime.fromisoformat(value)