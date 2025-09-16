async def test_user(auth_ac, db):
    response = await auth_ac["ac_client"].get(
        url="/users/get_me"
    )
    assert response.status_code == 200
    user_id = auth_ac["user"]["id"]

    response = await auth_ac["ac_client"].get(
        url=f"/users/{user_id}"
    )

    assert response.status_code == 200

    response = await auth_ac["ac_client"].post(
        url="/users/logout"
    )
    assert response.status_code == 200
    assert "access_token" not in auth_ac["ac_client"].cookies
