from typing import List, Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from werkzeug.security import generate_password_hash, check_password_hash
from .associations import UserRole

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone_number: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    
    roles: Mapped[List["Role"]] = relationship(secondary=UserRole, back_populates="users")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user", lazy="select")
    issued_tickets: Mapped[List["Ticket"]] = relationship(back_populates="cashier", lazy="select")
        
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!s}, email={self.email!r})"