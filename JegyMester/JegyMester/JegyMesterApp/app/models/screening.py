from datetime import datetime
from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime
from sqlalchemy import ForeignKey

class Screening(db.Model):
    __tablename__ = "screenings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    
    movie: Mapped["Movie"] = relationship(back_populates="screenings")
    room: Mapped["Room"] = relationship(back_populates="screenings")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="screening", lazy="select")

    def __repr__(self) -> str:
        return f"Screening(movie_id={self.movie_id}, time={self.start_time!s})"