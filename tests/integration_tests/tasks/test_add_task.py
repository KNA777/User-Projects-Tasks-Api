from src.schemas.tasks import TasksAdd


async def test_add_task(db):

    user_id = (await db.user.get_one(email="kot@pess.com")).id
    task = TasksAdd(title="some title",
                    description="some description",
                    assignee_id=user_id,
                    project_id=1,
                    status="todo")

    task_new = await db.task.add(task)
    assert task_new