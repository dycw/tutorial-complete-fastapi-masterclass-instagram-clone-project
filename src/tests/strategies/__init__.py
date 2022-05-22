from collections.abc import Iterator
from typing import Optional

from dycw_utilities.hypothesis import draw_and_flatmap
from dycw_utilities.hypothesis import draw_and_map
from dycw_utilities.hypothesis.sqlalchemy import sqlite_engines
from dycw_utilities.hypothesis.typing import MaybeSearchStrategy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import builds
from hypothesis.strategies import just
from hypothesis_faker.strategies import passwords
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.db.engines import yield_sess
from app.db.schemas.all import Base
from app.main import create_app
from app.models.main import ArticleBase
from app.models.main import UserBase


# generic


def apps() -> SearchStrategy[FastAPI]:
    """Strategy for generating FastAPI applications."""

    app = create_app()

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

    return draw_and_map(inner, sqlite_engines(base=Base))


def clients() -> SearchStrategy[TestClient]:
    """Strategy for generating Starlette test clients."""

    return apps().map(TestClient)


# schemas


def articles_base(
    *,
    content: MaybeSearchStrategy[Optional[str]] = None,
    creator_id: MaybeSearchStrategy[int],
) -> SearchStrategy[ArticleBase]:
    def inner(
        content: Optional[str], creator_id: int, /
    ) -> SearchStrategy[ArticleBase]:
        return builds(
            ArticleBase,
            **({} if content is None else {"content": just(content)}),
            creator_id=just(creator_id),
        )

    return draw_and_flatmap(inner, content, creator_id)


def users_base() -> SearchStrategy[UserBase]:
    return builds(UserBase, password=passwords())
