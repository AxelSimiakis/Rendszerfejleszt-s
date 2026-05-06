from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from .associations import UserRole

class Role(db.Model):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    users: Mapped[List["User"]] = relationship(secondary=UserRole, back_populates="roles")

    def __repr__(self) -> str:
        return f"Role(name={self.name!r})"