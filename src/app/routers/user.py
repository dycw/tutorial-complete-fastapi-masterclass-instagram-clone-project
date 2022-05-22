from dycw_utilities.fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from app.crud.users import create_user
from app.crud.users import delete_user
from app.crud.users import get_all_users
from app.crud.users import get_user
from app.crud.users import update_user
from app.db.engines import yield_sess
from app.db.schemas.users import DbUser
from app.models.main import UserBase
from app.models.main import UserDisplay


router = APIRouter(prefix="/user", tags=["user"])


# create


@router.post("/", response_model=UserDisplay)
def _(*, sess: Session = Depends(yield_sess), request: UserBase) -> DbUser:
    return create_user(sess=sess, request=request)


# read


@router.get("/", response_model=list[UserDisplay])
def _(*, sess: Session = Depends(yield_sess)) -> list[DbUser]:
    return get_all_users(sess=sess)


@router.get("/{id}", response_model=UserDisplay)
def _(*, sess: Session = Depends(yield_sess), id: int) -> DbUser | None:
    return get_user(sess=sess, id=id)


# update


@router.post("/{id}")
def _(
    *, sess: Session = Depends(yield_sess), id: int, request: UserBase
) -> bool:
    return update_user(sess=sess, id=id, request=request)


# delete


@router.post("/delete/{id}")
def _(*, sess: Session = Depends(yield_sess), id: int) -> bool:
    return delete_user(sess=sess, id=id)
