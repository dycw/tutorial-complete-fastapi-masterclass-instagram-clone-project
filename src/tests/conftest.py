from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient
from pytest import fixture

from app.db.database import Base
from app.db.database import create_sqlite_engine_and_session_cm
from app.db.database import yield_db
from app.main import app


@fixture(scope="function")
def test_client(*, tmp_path: Path) -> Iterator[TestClient]:
    test_engine, yield_test_db = create_sqlite_engine_and_session_cm(
        path=tmp_path.joinpath("db").as_posix()
    )
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[yield_db] = yield_test_db
    with TestClient(app) as client:
        yield client
