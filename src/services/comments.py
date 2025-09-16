from src.schemas.comments import CommentsRequest, CommentsAdd
from src.services.base import BaseService
from src.services.notifications import NotificationService


class CommentService(BaseService):


    async def create_comment_to_task(self, task_id, data: CommentsRequest, author_id):
        new_data = CommentsAdd(**data.model_dump(), task_id=task_id, author_id=author_id)
        created_comment = await self.db.comment.add(new_data)
        task = await self.db.task.get_one(id=task_id)
        author = await self.db.user.get_one(id=author_id)

        if task.assignee_id and task.assignee_id != author_id:
            await NotificationService.send_comment_notification(
                user_id=task.assignee_id,
                task_id=task_id,
                task_title=task.title,
                comment_content=data.content,
                author_name=author.username
            )
        return created_comment

    async def get_task_comments_by_id(self, task_id, limit, offset):
        comments = await self.db.comment.get_task_comments(task_id=task_id, limit=limit, offset=offset)
        return comments
