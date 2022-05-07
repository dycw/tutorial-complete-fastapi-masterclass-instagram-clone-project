from collections.abc import Iterator
from contextlib import AbstractContextManager
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from beartype import beartype
from fastapi import FastAPI
from fastapi.testclient import TestClient
from hypothesis.strategies import DrawFn
from hypothesis.strategies import composite
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.db.engines import yield_sess
from app.db.schemas.all import Base
from app.main import create_app


@composite
def temp_dirs(
    _: Any, /, *, path: Path | None = None
) -> AbstractContextManager[Path]:
    """Strategy for generating temporary directories."""

    @contextmanager
    @beartype
    def cm() -> Iterator[Path]:
        if path is None:
            with TemporaryDirectory() as temp:
                yield Path(temp)
        else:
            yield path

    return cm()


@composite
def engines(
    draw: DrawFn, /, *, path: Path | None = None
) -> AbstractContextManager[Engine]:
    """Strategy for generating SQLAlchemy engines."""

    @contextmanager
    @beartype
    def cm() -> Iterator[Engine]:
        with draw(temp_dirs(path=path)) as temp_dir:
            engine = create_engine(f"sqlite:///{temp_dir}/db.sqlite")
            with engine.begin() as conn:
                Base.metadata.create_all(bind=conn)
            yield engine

    return cm()


@composite
def apps(
    draw: DrawFn, /, *, path: Path | None = None
) -> AbstractContextManager[FastAPI]:
    """Strategy for generating FastAPI applications."""

    @contextmanager
    @beartype
    def cm() -> Iterator[FastAPI]:
        app = create_app()
        with draw(engines(path=path)) as engine:
            TestSession = sessionmaker(
                bind=engine, autoflush=False, autocommit=False
            )

            def yield_test_sess() -> Iterator[Session]:
                db = TestSession()
                try:
                    yield db
                finally:
                    db.close()

            app.dependency_overrides[yield_sess] = yield_test_sess
            yield app

    return cm()


@composite
def clients(
    draw: DrawFn, /, *, path: Path | None = None
) -> AbstractContextManager[TestClient]:
    """Strategy for generating Starlette test clients."""

    @contextmanager
    @beartype
    def cm() -> Iterator[TestClient]:
        with draw(apps(path=path)) as app:
            yield TestClient(app)

    return cm()
