from fastapi import FastAPI
from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.strategies import DataObject
from hypothesis.strategies import data
from hypothesis.strategies import integers
from hypothesis.strategies import text

from app.models.main import ArticleBase
from app.models.main import UserBase
from tests.strategies import apps
from tests.strategies import articles_base
from tests.strategies import clients
from tests.strategies import users_base


# generic


@given(app=apps())
def test_apps(app: FastAPI) -> None:
    assert isinstance(app, FastAPI)


@given(client=clients())
def test_clients(client: TestClient) -> None:
    assert isinstance(client, TestClient)


# schemas


@given(article=articles_base(creator_id=integers()))
def test_articles_base(article: ArticleBase) -> None:
    assert isinstance(article, ArticleBase)


@given(data=data(), content=text())
def test_articles_base_with_content(data: DataObject, content: str) -> None:
    article = data.draw(articles_base(content=content, creator_id=integers()))
    assert isinstance(article, ArticleBase)
    assert article.content == content


@given(user=users_base())
def test_users_base(user: UserBase) -> None:
    assert isinstance(user, UserBase)
