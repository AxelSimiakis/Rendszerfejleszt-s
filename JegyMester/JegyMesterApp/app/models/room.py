from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

class Room(db.Model):
    __tablename__ = "rooms"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    total_capacity: Mapped[int]
    
    seats: Mapped[List["Seat"]] = relationship(back_populates="room", lazy="select")
    screenings: Mapped[List["Screening"]] = relationship(back_populates="room", lazy="select")

    def __repr__(self) -> str:
        return f"Room(name={self.name!r}, capacity={self.total_capacity})"