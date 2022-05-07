from fastapi import FastAPI
from fastapi.testclient import TestClient
from hypothesis import given
from sqlalchemy.engine import Engine

from tests.strategies.strategies import apps
from tests.strategies.strategies import clients
from tests.strategies.strategies import sqlite_engines


@given(engine=sqlite_engines())
def test_sqlite_engines(engine: Engine) -> None:
    assert isinstance(engine, Engine)


@given(app=apps())
def test_apps(app: FastAPI) -> None:
    assert isinstance(app, FastAPI)


@given(client=clients())
def test_clients(client: TestClient) -> None:
    assert isinstance(client, TestClient)
