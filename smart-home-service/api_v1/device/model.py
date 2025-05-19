from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, String, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import Base

if TYPE_CHECKING:
    from ..home.model import Home

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    home_id: Mapped[int] = mapped_column(
        ForeignKey("home.id", ondelete="CASCADE"), nullable=False
    )
    device_type: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    model: Mapped[str] = mapped_column(String, nullable=True)
    full_address: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    home: Mapped["Home"] = relationship("Home", back_populates="devices")
