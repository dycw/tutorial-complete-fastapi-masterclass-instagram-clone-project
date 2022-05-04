from contextlib import AbstractContextManager

from beartype import beartype
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from app.db.database import yield_db
from app.db.db_user import create_user
from app.db.db_user import delete_user
from app.db.db_user import get_all_users
from app.db.db_user import get_user
from app.db.db_user import update_user
from app.db.models import DbUser
from app.schemas import UserBase
from app.schemas import UserDisplay


router = user_router = APIRouter(prefix="/user", tags=["user"])


# Create


@router.post("/", response_model=UserDisplay)
@beartype
def _(
    *,
    db: AbstractContextManager[Session] = Depends(yield_db),
    request: UserBase,
) -> DbUser:
    return create_user(db=db, request=request)


# Read


@router.get("/", response_model=list[UserDisplay])
@beartype
def _(
    *, db: AbstractContextManager[Session] = Depends(yield_db)
) -> list[DbUser]:
    return get_all_users(db=db)


@router.get("/{id}", response_model=UserDisplay)
@beartype
def _(
    *, db: AbstractContextManager[Session] = Depends(yield_db), id: int
) -> DbUser | None:
    return get_user(db=db, id=id)


# Update


@router.post("/{id}")
@beartype
def _(
    *,
    db: AbstractContextManager[Session] = Depends(yield_db),
    id: int,
    request: UserBase,
) -> bool:
    return update_user(db=db, id=id, request=request)


# Delete


@router.post("/delete/{id}")
@beartype
def _(
    *, db: AbstractContextManager[Session] = Depends(yield_db), id: int
) -> bool:
    return delete_user(db=db, id=id)
