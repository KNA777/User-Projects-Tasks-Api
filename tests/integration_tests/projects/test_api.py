async def test_projects(db, auth_ac):
    response = await auth_ac["ac_client"].post(
        url="/projects",
        json={
            "name": "project_from_test",
            "description": "some description",
        }
    )
    project_id = response.json()["id"]
    assert response.status_code == 200

    new_description = "new_patch_description"
    new_name = "new_patch_name"
    update_response = await auth_ac["ac_client"].patch(
        url=f"/projects/edit/{project_id}",
        json={
            "name": new_name,
            "description": new_description
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == new_description
    assert update_response.json()["name"] == new_name

    user_projects = await auth_ac["ac_client"].get(
        url="/projects"
    )

    assert user_projects.status_code == 200
    user_projects = user_projects.json()
    assert isinstance(user_projects, dict)
    assert isinstance(user_projects["projects"], list)






