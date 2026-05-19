from sqlalchemy import BigInteger, String, Double
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, default="")
    balance: Mapped[float] = mapped_column(Double, default=0.0)
