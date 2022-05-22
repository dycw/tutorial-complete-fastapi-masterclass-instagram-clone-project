from fastapi.testclient import TestClient
from hypothesis import given
from starlette.status import HTTP_200_OK

from app.routers.product import product
from tests.strategies import clients


# read


@given(client=clients())
def test_get(client: TestClient) -> None:
    r = client.get("/product/all")
    assert r.status_code == HTTP_200_OK
    assert r.json() == product
