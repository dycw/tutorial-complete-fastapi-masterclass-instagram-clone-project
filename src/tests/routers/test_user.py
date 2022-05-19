from fastapi.testclient import TestClient
from hypothesis import given
from starlette.status import HTTP_200_OK

from app.models.main import UserBase
from tests.strategies.strategies import clients
from tests.strategies.user import users_base


# create


@given(client=clients(), user=users_base())
def test_post(client: TestClient, user: UserBase) -> None:
    rp = client.post("/user/", data=user.json())
    assert rp.status_code == HTTP_200_OK, rp.text
    assert rp.json() == {
        "username": user.username,
        "email": user.email,
        "items": [],
    }

    rg = client.get("/user/")
    assert rg.status_code == HTTP_200_OK, rg.text
    assert rg.json() == [
        {"username": user.username, "email": user.email, "items": []}
    ]


# read


@given(client=clients())
def test_get(client: TestClient) -> None:
    r = client.get("/user/")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() == []


@given(client=clients(), user=users_base())
def test_get_detail_existing(client: TestClient, user: UserBase) -> None:
    _ = client.post("/user/", data=user.json())
    r = client.get("/user/1")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() == {
        "username": user.username,
        "email": user.email,
        "items": [],
    }


@given(client=clients())
def test_get_detail_non_existent(client: TestClient) -> None:
    r = client.get("/user/1")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() is None


# update


@given(client=clients(), first=users_base(), second=users_base())
def test_update(client: TestClient, first: UserBase, second: UserBase) -> None:
    _ = client.post("/user/", data=first.json())
    _ = client.post("/user/1", data=second.json())
    r = client.get("/user/1")
    assert r.json() == {
        "username": second.username,
        "email": second.email,
        "items": [],
    }


# delete


@given(client=clients(), user=users_base())
def test_delete(client: TestClient, user: UserBase) -> None:
    _ = client.post("/user/", data=user.json())
    r = client.post("/user/delete/1")
    assert r.json() is True
