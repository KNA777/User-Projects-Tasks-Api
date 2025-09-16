async def test_comments(auth_ac, db):
    project_id = (await db.project.get_all())[0].id
    user_id = (await db.user.get_all())[0].id
    response = await auth_ac["ac_client"].post(
        url=f"/tasks/add/project/{project_id}",
        json={
            "title": "title",
            "description": "description",
            "assignee_id": user_id
        }
    )
    assert response.status_code == 200
    task_id = (await db.task.get_all())[0].id
    response = await auth_ac["ac_client"].post(
        url=f"/comments/add/tasks/{task_id}",
        json={
            "content": "new_content"
        }
    )

    assert response.status_code == 200

    response = await auth_ac["ac_client"].get(
        url=f"/comments/get/tasks/{task_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



