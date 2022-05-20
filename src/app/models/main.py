from pydantic import BaseModel
from pydantic import EmailStr


class Article(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDisplay(BaseModel):
    username: str
    email: EmailStr
    items: list[Article] = []

    class Config:
        orm_mode = True


class User(BaseModel):  # user inside ArticleBase
    id: int
    username: str

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int


class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config:
        orm_mode = True
