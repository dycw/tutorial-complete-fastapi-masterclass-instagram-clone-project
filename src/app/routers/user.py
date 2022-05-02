from contextlib import AbstractContextManager

from beartype import beartype
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.db_user import create_user
from app.db.models import DbUser
from app.schemas import UserBase


router = user_router = APIRouter(prefix="/user", tags=["user"])


# Create


@router.post("/")
@beartype
def _(
    *, db: AbstractContextManager[Session] = Depends(get_db), request: UserBase
) -> DbUser:
    return create_user(db=db, request=request)


# Read


# Update

# Delete
