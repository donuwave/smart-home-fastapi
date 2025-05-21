from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from pgvector.sqlalchemy import Vector

from config import Base

if TYPE_CHECKING:
    from ..home.model import Home

class Face(Base):
    __tablename__ = 'faces'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    home_id: Mapped[int] = mapped_column(
        ForeignKey("home.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String)
    embedding: Mapped[List[float]] = mapped_column(Vector(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    home: Mapped["Home"] = relationship("Home", back_populates="faces")