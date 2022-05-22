from re import DOTALL
from re import search

from fastapi.testclient import TestClient
from hypothesis import given
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_404_NOT_FOUND

from tests.strategies import clients


# read


@given(client=clients())
def test_get(client: TestClient) -> None:
    r = client.get("/product/all")
    assert r.status_code == HTTP_200_OK
    assert r.text == "watch camera phone"


@given(client=clients())
def test_get_detail(client: TestClient) -> None:
    r = client.get("/product/1")
    assert r.status_code == HTTP_200_OK
    assert search("<html>.*</html>", r.text.strip("\n"), flags=DOTALL)


@given(client=clients())
def test_get_detail_non_existent(client: TestClient) -> None:
    r = client.get("/product/3")
    assert r.status_code == HTTP_404_NOT_FOUND
    assert r.text == "Product not available"
