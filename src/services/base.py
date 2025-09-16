from src.context_manager_db.context_manager import DBManager


class BaseService:

    db: DBManager | None


    def __init__(self, db: DBManager | None = None):
        self.db = db