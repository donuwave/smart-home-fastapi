from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import String, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api_v1.profile import Profile
from config.base_model import Base


class User(Base):
    __tablename__ = "user"
    email: Mapped[EmailStr] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    profile: Mapped["Profile"] = relationship(back_populates="user")
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"), unique=True, nullable=False
    )
