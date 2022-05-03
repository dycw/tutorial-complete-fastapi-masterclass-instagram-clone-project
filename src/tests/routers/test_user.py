from beartype import beartype
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK


@beartype
def test_hello(test_client: TestClient) -> None:
    r = test_client.post(
        "/users/", json={"username": "a", "email": "e", "password": "p"}
    )
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() == {"Hello": "World"}
