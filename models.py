from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50))

    email: Mapped[str] = mapped_column(String(100), unique=True)

    password: Mapped[str] = mapped_column(String(255))
    

class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    url: Mapped[str] = mapped_column(
        String(500)
    )

    product_name: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    price: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    rating: Mapped[str] = mapped_column(
        String(20),
        default=""
    )
