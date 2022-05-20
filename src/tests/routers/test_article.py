from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.strategies import DataObject
from hypothesis.strategies import data
from starlette.status import HTTP_200_OK

from app.models.main import UserBase
from tests.strategies import articles_base
from tests.strategies import clients
from tests.strategies import users_base


# create


@given(data=data(), client=clients(), user=users_base())
def test_post(data: DataObject, client: TestClient, user: UserBase) -> None:
    rpu = client.post("/user/", data=user.json())
    assert rpu.status_code == HTTP_200_OK, rpu.text

    article = data.draw(articles_base(creator_id=1))
    rpa = client.post("/article/", data=article.json())
    assert rpa.status_code == HTTP_200_OK, rpa.text
    assert rpa.json() == {
        "title": article.title,
        "content": article.content,
        "published": article.published,
        "user": {"id": 1, "username": user.username},
    }

    rg = client.get("/article/1")
    assert rg.status_code == HTTP_200_OK, rg.text
    assert rg.json() == {
        "title": article.title,
        "content": article.content,
        "published": article.published,
        "user": {"id": 1, "username": user.username},
    }


# read


@given(client=clients())
def test_get_detail_non_existent(client: TestClient) -> None:
    r = client.get("/article/1")
    assert r.status_code == HTTP_200_OK, r.text
    assert r.json() is None
