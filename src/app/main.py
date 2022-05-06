from beartype import beartype

from app.init.setup import create_app


app = create_app()


@app.get("/hello/")
@beartype
def _() -> dict[str, str]:
    return {"Hello": "World"}
