from typing import Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey

class Ticket(db.Model):
    __tablename__ = "tickets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    screening_id: Mapped[int] = mapped_column(ForeignKey("screenings.id"))
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"))
    
    issued_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default="valid")
    transaction: Mapped["Transaction"] = relationship(back_populates="tickets")
    screening: Mapped["Screening"] = relationship(back_populates="tickets")
    seat: Mapped["Seat"] = relationship(back_populates="tickets")
    cashier: Mapped[Optional["User"]] = relationship(back_populates="issued_tickets")

    def __repr__(self) -> str:
        return f"Ticket(id={self.id}, screening_id={self.screening_id}, status={self.status!r})"