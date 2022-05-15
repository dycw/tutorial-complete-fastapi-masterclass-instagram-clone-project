from contextlib import AbstractContextManager
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from hypothesis import given
from sqlalchemy.engine import Engine

from tests.strategies.strategies import apps
from tests.strategies.strategies import clients
from tests.strategies.strategies import engines
from tests.strategies.strategies import temp_dirs


@given(temp_dirs=temp_dirs())
def test_temp_dirs(temp_dirs: AbstractContextManager[Path]) -> None:
    with temp_dirs as temp_dir:
        assert isinstance(temp_dir, Path)
        assert temp_dir.is_dir()
        assert temp_dir.exists()


@given(engines=engines())
def test_engines(engines: AbstractContextManager[Engine]) -> None:
    with engines as engine:
        assert isinstance(engine, Engine)


@given(apps=apps())
def test_apps(apps: AbstractContextManager[FastAPI]) -> None:
    with apps as app:
        assert isinstance(app, FastAPI)


@given(clients=clients())
def test_clients(clients: AbstractContextManager[TestClient]) -> None:
    with clients as client:
        assert isinstance(client, TestClient)
