from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.strategies import builds
from hypothesis_faker import passwords
from starlette.status import HTTP_200_OK

from app.models.main import UserBase
from tests.strategies.strategies import clients


# create


@given(client=clients(), user=builds(UserBase, password=passwords()))
def test_post(client: TestClient, user: UserBase) -> None:
    rp = client.post("/user/", data=user.json())
    assert rp.status_code == HTTP_200_OK, rp.text
    assert list(rp.json()) == ["username", "email", "items"]

    rg = client.get("/user/")
    assert rg.status_code == HTTP_200_OK, rg.text
    assert isinstance(res := rg.json(), list)
    assert len(res) == 1
    assert list(res[0]) == ["username", "email", "items"]


# read


@given(client=clients())
def test_get(client: TestClient) -> None:
    r = client.get("/user/")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() == []


@given(client=clients())
def test_get_detail(client: TestClient) -> None:
    r = client.get("/user/")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() == []
