from sqlalchemy import select

from src.models import CommentsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.comments import CommentMapper
from src.schemas.comments import CommentsWithOutTaskId


class CommentRepository(BaseRepository):

    model = CommentsOrm
    mapper = CommentMapper


    async def get_task_comments(self, task_id, limit, offset):
        query = (select(self.model)
                 .filter_by(task_id=task_id)
                 .limit(limit)
                 .offset(offset))
        comments = await self.session.execute(query)
        return [CommentsWithOutTaskId.model_validate(model, from_attributes=True) for model in comments.scalars().all()]