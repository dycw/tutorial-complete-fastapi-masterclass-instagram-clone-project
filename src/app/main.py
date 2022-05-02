from beartype import beartype
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.db.database import engine
from app.db.models import Base
from app.routers.blog_get import blog_get_router
from app.routers.blog_post import blog_post_router


app = FastAPI()
app.include_router(blog_get_router)
app.include_router(blog_post_router)


@app.get("/hello/")
@beartype
def _() -> JSONResponse:
    return JSONResponse({"Hello": "World"})


Base.metadata.create_all(engine)
