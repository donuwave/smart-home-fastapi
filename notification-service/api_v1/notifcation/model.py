from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from config import Base


class Notification(Base):
    home_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
