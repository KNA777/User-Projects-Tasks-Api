from src.schemas.projects import ProjectAdd


async def test_db_add(db):
    #add project
    user = await db.user.get_one(email="kot@pess.com")
    result = ProjectAdd(name="Project1",
                        description="some",
                        owner_id=user.id)

    project = await db.project.add(result)
    assert project