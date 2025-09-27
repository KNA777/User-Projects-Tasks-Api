from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db_config import BaseOrm


class UsersOrm(BaseOrm):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)

    projects: Mapped[list["ProjectsOrm"]] = relationship(
        back_populates="user"
    )

