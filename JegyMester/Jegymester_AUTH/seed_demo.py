from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.movie import Movie
from app.models.room import Room
from app.models.seat import Seat
from app.models.screening import Screening

app = create_app()

with app.app_context():
    db.create_all()

    movie = Movie.query.filter_by(title="Demo film").first()
    if not movie:
        movie = Movie(title="Demo film", description="Teszt vetítés a frontend kipróbálásához", duration_minutes=110)
        db.session.add(movie)
        db.session.flush()

    room = Room.query.filter_by(name="Demo terem").first()
    if not room:
        room = Room(name="Demo terem", total_capacity=50)
        db.session.add(room)
        db.session.flush()

    for row in range(1, 6):
        for seat_num in range(1, 11):
            exists = Seat.query.filter_by(room_id=room.id, row_num=row, seat_num=seat_num).first()
            if not exists:
                db.session.add(Seat(room_id=room.id, row_num=row, seat_num=seat_num))

    screening = Screening.query.filter_by(movie_id=movie.id, room_id=room.id).first()
    if not screening:
        db.session.add(Screening(movie_id=movie.id, room_id=room.id, start_time=(datetime.now() + timedelta(days=1)).isoformat()))

    db.session.commit()
    print("Demo adatok letrehozva: film, terem, 50 szek, vetites")
