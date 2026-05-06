from datetime import datetime
from typing import List
from decimal import Decimal
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, DateTime, Numeric
from sqlalchemy import ForeignKey

class Transaction(db.Model):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    purchase_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    payment_method: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="success")
    
    user: Mapped["User"] = relationship(back_populates="transactions")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="transaction", lazy="select")

    def __repr__(self) -> str:
        return f"Transaction(id={self.id}, amount={self.total_amount}, status={self.status!r})"