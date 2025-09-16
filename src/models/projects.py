import typing

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db_config import BaseOrm
from src.models import UsersOrm

if typing.TYPE_CHECKING:
    from src.models import TasksOrm

class ProjectsOrm(BaseOrm):

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["UsersOrm"] = relationship(
        back_populates="projects"
    )
    tasks: Mapped[list["TasksOrm"]] = relationship(
        back_populates="projects"
    )
