from src.models import ProjectsOrm, CommentsOrm
from src.repositories.mapper.base import DataMapper
from src.schemas.comments import Comments
from src.schemas.projects import Projects


class CommentMapper(DataMapper):

    db_model = CommentsOrm
    schema = Comments
