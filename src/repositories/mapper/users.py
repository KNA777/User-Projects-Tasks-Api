from src.models import UsersOrm
from src.repositories.mapper.base import DataMapper
from src.schemas.users import User


class UserMapper(DataMapper):

    db_model = UsersOrm
    schema = User



