async def test_task(auth_ac, db):
    project_id = (await db.project.get_all())[0].id
    user_id = (await db.user.get_all())[0].id
    assert project_id
    assert user_id
    new_title = "new title"
    new_description = "new description"

    response = await auth_ac["ac_client"].post(
        url=f"/tasks/add/project/{project_id}",
        json={
            "title": new_title,
            "description": new_description,
            "assignee_id": user_id
        }
    )
    new_task = response.json()
    assert response.status_code == 200
    assert new_task["title"] == new_title
    assert new_task["description"] == new_description


    updated_title = "updated title"
    updated_description = "updated description"

    task_id = new_task["id"]

    response = await auth_ac["ac_client"].patch(
        url=f"/tasks/edit/{task_id}",
        json={
            "title": updated_title,
            "description": updated_description,
            "assignee_id": user_id
        },
        params={
            "status": "in_progress"
        }
    )
    edit_task = response.json()
    task_id = edit_task["id"]

    assert response.status_code == 200
    assert edit_task["title"] == updated_title
    assert edit_task["description"] == updated_description


    response = await auth_ac["ac_client"].delete(
        url=f"/tasks/delete/{task_id}")

    assert response.status_code == 200

    project_id = edit_task["project_id"]
    response = await auth_ac["ac_client"].get(
        url=f"/tasks/get/projects/{project_id}")

    data = response.json()
    assert response.status_code == 200
    assert data
