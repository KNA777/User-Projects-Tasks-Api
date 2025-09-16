from enum import StrEnum

import typing
from sqlalchemy import String, ForeignKey, Text, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db_config import BaseOrm

if typing.TYPE_CHECKING:
    from src.models import ProjectsOrm, CommentsOrm


class TaskStatus(StrEnum):
    """Статусы задачи"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TasksOrm(BaseOrm):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus,
             values_callable=lambda x: [e.value for e in TaskStatus],
             name="task_status_enum"),
        default=TaskStatus.TODO,
        nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )
    assignee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    projects: Mapped["ProjectsOrm"] = relationship(
        back_populates="tasks"
    )

    comments: Mapped[list["CommentsOrm"]] = relationship(
        back_populates="tasks"
    )
