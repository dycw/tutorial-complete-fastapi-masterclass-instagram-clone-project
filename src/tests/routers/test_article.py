from fastapi.testclient import TestClient
from hypothesis import given
from starlette.status import HTTP_200_OK

from tests.strategies import articles_base
from tests.strategies import clients


# create


@given(client=clients(), article=articles_base())
def test_post(client: TestClient) -> None:
    r = client.get("/article/")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() == []
    assert 0


# read


@given(client=clients())
def test_get(client: TestClient) -> None:
    r = client.get("/article/")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() == []
    assert 0
