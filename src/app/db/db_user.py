from contextlib import AbstractContextManager

from beartype import beartype
from sqlalchemy.orm import Session

from app.db.hash import Hash
from app.db.models import DbUser
from app.schemas import UserBase


@beartype
def create_user(
    *, db: AbstractContextManager[Session], request: UserBase
) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    with db as sess:
        sess.add(new_user)
        sess.commit()
        sess.refresh(new_user)
    return new_user
