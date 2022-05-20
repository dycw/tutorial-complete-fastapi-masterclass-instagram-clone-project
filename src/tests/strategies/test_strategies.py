from fastapi import FastAPI
from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.strategies import integers
from sqlalchemy.engine import Engine

from app.models.main import ArticleBase
from app.models.main import UserBase
from tests.strategies import apps
from tests.strategies import articles_base
from tests.strategies import clients
from tests.strategies import sqlite_engines
from tests.strategies import users_base


# generic


@given(engine=sqlite_engines())
def test_sqlite_engines(engine: Engine) -> None:
    assert isinstance(engine, Engine)


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


@given(user=users_base())
def test_users_base(user: UserBase) -> None:
    assert isinstance(user, UserBase)
