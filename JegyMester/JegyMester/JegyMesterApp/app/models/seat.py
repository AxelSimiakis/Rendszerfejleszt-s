from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Seat(db.Model):
    __tablename__ = "seats"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    row_num: Mapped[int]
    seat_num: Mapped[int]
    
    room: Mapped["Room"] = relationship(back_populates="seats")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="seat", lazy="select")

    def __repr__(self) -> str:
        return f"Seat(room_id={self.room_id}, row={self.row_num}, seat={self.seat_num})"