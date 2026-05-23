from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.types import UserID, DeviceID


class User(Base):
    __tablename__ = "users"

    id: Mapped[UserID] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[DeviceID] = mapped_column(String, unique=True, nullable=False)
