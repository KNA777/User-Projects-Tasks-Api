from src.models import UsersOrm
from src.services.base import BaseService
from src.utils import check_permissions, check_superuser_permission


class UserService(BaseService):

    async def get_all_users(self, current_user):
        check_superuser_permission(current_user)
        return await self.db.user.get_all()

    async def get_user_for_dependencies(self, user_id_get):
        return await self.db.user.get_one(id=user_id_get)

    async def get_user_by_id_with_projects(self, current_user: UsersOrm, user_id_get):
        check_permissions(current_user=current_user, user_id=user_id_get)
        return await self.db.user.get_user_with_projects(user_id=user_id_get)

    async def edit_me(self, data, current_user, user_id):
        check_permissions(current_user=current_user, user_id=user_id)
        return await self.db.user.edit(data=data, id=user_id, exclude_unset=True)

    async def delete_me(self, current_user, user_id):
        check_permissions(current_user=current_user, user_id=user_id)
        return await self.db.user.delete(id=user_id)

    async def get_user(self, **filter_by):
        return await self.db.user.get_one(**filter_by)
