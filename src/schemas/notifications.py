from pydantic import BaseModel
from datetime import datetime

class TaskAssignedNotification(BaseModel):
    """Уведомление о назначении задачи"""
    type: str = "task_assigned"
    message: str
    task_id: int
    task_title: str
    project_name: str
    timestamp: str

class CommentAddedNotification(BaseModel):
    """Уведомление о новом комментарии"""
    type: str = "comment_added"
    message: str
    task_id: int
    task_title: str
    comment_content: str  # Первые 100 символов
    author_name: str
    timestamp: str