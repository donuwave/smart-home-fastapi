from sqlalchemy import Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config import Base


from ..device.model import Device


class Home(Base):
    __tablename__ = 'home'

    id: Mapped[int]    = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer)
    invited_users_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    devices: Mapped[list["Device"]] = relationship(
        "Device", back_populates="home", cascade="all, delete-orphan"
    )