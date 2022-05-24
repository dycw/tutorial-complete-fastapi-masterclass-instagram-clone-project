import datetime as dt
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose.jwt import encode


token_key = "token"  # noqa: S105
oauth2_scheme = OAuth2PasswordBearer(token_key)


SECRET_KEY = "deda33fb31a7cd84a646d2bacf52bdb87cf7cc7fdac9382fbb33c9b06de9b323"  # noqa: E501, S105
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict, expires_delta: Optional[dt.timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = dt.datetime.utcnow() + expires_delta
    else:
        expire = dt.datetime.utcnow() + dt.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
