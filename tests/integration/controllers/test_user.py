from http import HTTPStatus
from src.app import User, db, Role


def test_get_user_sucess(client):
    # given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="jhon doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # when
    response = client.get(f"/users/{user.id}")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json == [{"id": user.id, "username": user.username}]


def test_list_users(client):
    # given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="jhon doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )
    access_token = response.json["access_token"]

    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {access_token}"}
    )

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": {
                    "id": user.role.id,
                    "name": user.role.name,
                },
            }
        ]
    }
