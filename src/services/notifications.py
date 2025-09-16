# src/services/notifications.py
from src.services.sse_manager import sse_manager
from src.schemas.notifications import TaskAssignedNotification, CommentAddedNotification
from datetime import datetime


class NotificationService:
    """Сервис для отправки уведомлений через SSE"""

    @staticmethod
    async def send_task_assigned_notification(
            user_id: int,
            task_id: int,
            task_title: str,
            project_name: str
    ):
        """Отправляет уведомление о назначении задачи"""
        notification = TaskAssignedNotification(
            message=f"Вам назначена новая задача: '{task_title}' в проекте '{project_name}'",
            task_id=task_id,
            task_title=task_title,
            project_name=project_name,
            timestamp=datetime.now().isoformat()
        )
        await sse_manager.send_event(user_id, notification.model_dump())

    @staticmethod
    async def send_comment_notification(
            user_id: int,
            task_id: int,
            task_title: str,
            comment_content: str,
            author_name: str
    ):
        """Отправляет уведомление о новом комментарии"""

        truncated_comment = comment_content[:100] + "..." if len(comment_content) > 100 else comment_content

        notification = CommentAddedNotification(
            message=f"Новый комментарий к задаче '{task_title}'",
            task_id=task_id,
            task_title=task_title,
            comment_content=truncated_comment,
            author_name=author_name,
            timestamp=datetime.now().isoformat()
        )
        await sse_manager.send_event(user_id, notification.model_dump())
