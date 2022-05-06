from beartype import beartype
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from app.db.db_user import create_user
from app.db.db_user import delete_user
from app.db.db_user import get_all_users
from app.db.db_user import get_user
from app.db.db_user import update_user
from app.db.engines import yield_sess
from app.db.models import DbUser
from app.schemas import UserBase
from app.schemas import UserDisplay


router = user_router = APIRouter(prefix="/user", tags=["user"])


# Create


@router.post("/", response_model=UserDisplay)
@beartype
def _(*, sess: Session = Depends(yield_sess), request: UserBase) -> DbUser:
    return create_user(sess=sess, request=request)


# Read


@router.get("/", response_model=list[UserDisplay])
@beartype
def _(*, sess: Session = Depends(yield_sess)) -> list[DbUser]:
    return get_all_users(sess=sess)


@router.get("/{id}", response_model=UserDisplay)
@beartype
def _(*, sess: Session = Depends(yield_sess), id: int) -> DbUser | None:
    return get_user(sess=sess, id=id)


# Update


@router.post("/{id}")
@beartype
def _(
    *, sess: Session = Depends(yield_sess), id: int, request: UserBase
) -> bool:
    return update_user(sess=sess, id=id, request=request)


# Delete


@router.post("/delete/{id}")
@beartype
def _(*, sess: Session = Depends(yield_sess), id: int) -> bool:
    return delete_user(sess=sess, id=id)
