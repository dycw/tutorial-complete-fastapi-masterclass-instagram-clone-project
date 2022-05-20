from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


SQLITE_ENGINE = create_engine("sqlite:///./db.sqlite3")
SessionLocal = sessionmaker(
    bind=SQLITE_ENGINE, autoflush=False, autocommit=False
)


def yield_sess() -> Iterator[Session]:  # pragma: no cover
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
