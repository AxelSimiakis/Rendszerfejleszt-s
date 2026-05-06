from typing import List, Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Text

class Movie(db.Model):
    __tablename__ = "movies"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text)
    duration_minutes: Mapped[Optional[int]]
    
    screenings: Mapped[List["Screening"]] = relationship(back_populates="movie", lazy="select")

    def __repr__(self) -> str:
        return f"Movie(title={self.title!r})"