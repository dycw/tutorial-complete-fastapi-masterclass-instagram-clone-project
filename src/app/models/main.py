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


class User(BaseModel):
    id: int
    username: str


class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int


class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    creator: int
    user: User

    class Config:
        orm_mode = True
