from src.repositories.comments import CommentRepository
from src.repositories.projects import ProjectRepository
from src.repositories.tasks import TaskRepository
from src.repositories.users import UserRepository


class DBManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UserRepository(self.session)
        self.project = ProjectRepository(self.session)
        self.task = TaskRepository(self.session)
        self.comment = CommentRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
