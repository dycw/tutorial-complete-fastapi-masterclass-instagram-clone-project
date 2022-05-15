from contextlib import AbstractContextManager

from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.strategies import builds
from hypothesis_faker import passwords
from starlette.status import HTTP_200_OK

from app.models.main import UserBase
from tests.strategies.strategies import clients


# create


@given(clients=clients(), user=builds(UserBase, password=passwords()))
def test_post(
    clients: AbstractContextManager[TestClient], user: UserBase
) -> None:
    with clients as client:
        rp = client.post("/user/", data=user.json())
        assert rp.status_code == HTTP_200_OK, rp.text
        assert list(rp.json()) == ["username", "email", "items"]

        rg = client.get("/user/")
        assert rg.status_code == HTTP_200_OK, rg.text
        assert isinstance(res := rg.json(), list)
        assert len(res) == 1
        assert list(res[0]) == ["username", "email", "items"]


# read


@given(clients=clients())
def test_get(clients: AbstractContextManager[TestClient]) -> None:
    with clients as client:
        r = client.get("/user/")
        assert r.status_code == HTTP_200_OK, r.text
        assert r.json() == []


@given(clients=clients())
def test_get_detail(clients: AbstractContextManager[TestClient]) -> None:
    with clients as client:
        r = client.get("/user/")
        assert r.status_code == HTTP_200_OK, r.text
        assert r.json() == []
