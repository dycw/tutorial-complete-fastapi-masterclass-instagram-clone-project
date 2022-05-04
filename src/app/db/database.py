from collections.abc import Callable
from collections.abc import Iterator
from contextlib import AbstractContextManager
from contextlib import contextmanager

from beartype import beartype
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


@beartype
def create_sqlite_engine_and_session_cm(
    *, path: str
) -> tuple[Engine, Callable[..., AbstractContextManager[Session]]]:
    url = f"sqlite:///{path}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    @contextmanager
    @beartype
    def yield_session() -> Iterator[Session]:
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    return engine, yield_session


ENGINE, yield_db = create_sqlite_engine_and_session_cm(path="./db.sqlite3")
Base = declarative_base()
