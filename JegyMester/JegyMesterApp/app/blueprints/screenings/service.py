from app.extensions import db
from app.models.screening import Screening
from app.models.movie import Movie
from sqlalchemy import select
from .schemas import ScreeningResponseSchema
from datetime import datetime, timedelta
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
            room_id = data.get('room_id')
            movie_id = data.get('movie_id')
            
            if start_time_str:
                data['start_time'] = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
            
            start_time = data['start_time']

            movie = db.session.get(Movie, movie_id)
            if not movie:
                return False, "Film nem talalhato"

            duration_minutes = movie.duration_minutes or 0
            end_time = start_time + timedelta(minutes=duration_minutes)

            existing_screenings = db.session.execute(
                select(Screening)
                .join(Movie)
                .filter(Screening.room_id == room_id)
            ).scalars().all()
            
            for existing_screening in existing_screenings:
                existing_start = existing_screening.start_time
                existing_duration = existing_screening.movie.duration_minutes or 0
                existing_end = existing_start + timedelta(minutes=existing_duration)

                if start_time < existing_end and end_time > existing_start:
                    return False, (f"A terem foglalt ebben az idopontban. "
                                 f"Letezik vetites {existing_start.strftime('%Y-%m-%d %H:%M:%S')}-tol "
                                 f"{existing_end.strftime('%Y-%m-%d %H:%M:%S')}-ig")

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
            
            # adtak-e el jegyet a vetitesre
            if screening.tickets:
                return False, f"Vetites nem torolheto, mert {len(screening.tickets)} jegy el lett adva ra"
            
            db.session.delete(screening)
            db.session.commit()
            return True, "Vetites sikeresen torolve"
        except Exception as ex:
            db.session.rollback()
            print(f"Torlesi hiba: {ex}")
            return False, str(ex)