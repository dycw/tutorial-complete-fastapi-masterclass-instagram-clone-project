from beartype import beartype
from fastapi.responses import JSONResponse

from app.db.database import ENGINE
from app.db.models import Base
from app.init.setup import create_app


app = create_app()


@app.get("/hello/")
@beartype
def _() -> JSONResponse:
    return JSONResponse({"Hello": "World"})


Base.metadata.create_all(ENGINE)
