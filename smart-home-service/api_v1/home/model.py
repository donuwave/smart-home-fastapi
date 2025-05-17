from sqlalchemy import Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from config import Base

class Home(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer)
    invited_users_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))