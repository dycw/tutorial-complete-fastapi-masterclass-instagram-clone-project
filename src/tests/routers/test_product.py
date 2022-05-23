from re import DOTALL
from re import search

from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.strategies import characters
from hypothesis.strategies import lists
from hypothesis.strategies import text
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_404_NOT_FOUND

from tests.strategies import clients


@given(client=clients())
def test_all(client: TestClient) -> None:
    r = client.get("/product/all")
    assert r.status_code == HTTP_200_OK
    assert r.text == "watch camera phone"


@given(
    client=clients(),
    header=text(characters(blacklist_categories=["Z", "C"])),
    headers=lists(text(characters(blacklist_categories=["C"]))),
)
def test_with_header(
    client: TestClient, header: str, headers: list[str]
) -> None:
    r = client.get(
        "/product/withheader",
        headers={"custom-header": header, "custom-headers": ",".join(headers)},
    )
    assert r.status_code == HTTP_200_OK
    assert r.headers["custom_response_header"] == ",".join(headers)
    assert r.request.headers["custom-header"] == header
    assert r.request.headers["custom-headers"] == ",".join(headers)


@given(client=clients())
def test_detail(client: TestClient) -> None:
    r = client.get("/product/1")
    assert r.status_code == HTTP_200_OK
    assert search("<html>.*</html>", r.text.strip("\n"), flags=DOTALL)


@given(client=clients())
def test_detail_non_existent(client: TestClient) -> None:
    r = client.get("/product/3")
    assert r.status_code == HTTP_404_NOT_FOUND
    assert r.text == "Product not available"
