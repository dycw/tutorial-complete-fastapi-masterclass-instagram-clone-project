from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.database import Base


class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
