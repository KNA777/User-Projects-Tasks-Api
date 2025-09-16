import shutil

from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_avatar


class AvatarService(BaseService):

    async def load_avatar(self, user_id, file: UploadFile):

        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(fsrc=file.file, fdst=new_file)

        resize_avatar.delay(image_path)

        await self.db.user.load_new_user_avatar_to_db(user_id=user_id, avatar_url=image_path)

        return {"status": "Task in progress"}