from beartype import beartype
from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes="bcrypt", deprecated="auto")


class Hash:
    @staticmethod
    @beartype
    def bcrypt(password: str) -> str:
        return pwd_cxt.hash(password)

    @staticmethod
    @beartype
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_cxt.verify(plain_password, hashed_password)
