from collections.abc import Iterator
from pathlib import Path
from typing import Union

from beartype import beartype
from dycw_utilities.hypothesis import draw_and_map
from dycw_utilities.hypothesis.sqlalchemy import (
    sqlite_engines as _sqlite_engines,
)
from dycw_utilities.hypothesis.tempfile import temp_dirs
from dycw_utilities.hypothesis.typing import MaybeSearchStrategy
from dycw_utilities.tempfile import TemporaryDirectory
from fastapi import FastAPI
from fastapi.testclient import TestClient
from hypothesis.strategies import SearchStrategy
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.db.engines import yield_sess
from app.db.schemas.all import Base
from app.main import create_app


@beartype
def sqlite_engines(
    *, dir: MaybeSearchStrategy[Union[Path, TemporaryDirectory]] = temp_dirs()
) -> SearchStrategy[Engine]:
    """Strategy for generating SQLAlchemy engines."""

    @beartype
    def post_init(engine: Engine, /) -> None:
        with engine.begin() as conn:
            Base.metadata.create_all(bind=conn)  # type: ignore

    return _sqlite_engines(dir=dir, post_init=post_init)


@beartype
def apps(
    *, dir: MaybeSearchStrategy[Union[Path, TemporaryDirectory]] = temp_dirs()
) -> SearchStrategy[FastAPI]:
    """Strategy for generating FastAPI applications."""

    app = create_app()

    @beartype
    def inner(engine: Engine, /) -> FastAPI:
        TestSession = sessionmaker(
            bind=engine, autoflush=False, autocommit=False
        )

        def yield_test_sess() -> Iterator[Session]:  # do not beartype
            db = TestSession()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[yield_sess] = yield_test_sess
        return app

    return draw_and_map(inner, sqlite_engines(dir=dir))


@beartype
def clients(
    *, dir: MaybeSearchStrategy[Union[Path, TemporaryDirectory]] = temp_dirs()
) -> SearchStrategy[TestClient]:
    """Strategy for generating Starlette test clients."""

    return apps(dir=dir).map(TestClient)
