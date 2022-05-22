from dycw_utilities.fastapi import APIRouter


router = APIRouter(prefix="/product", tags=["product"])


product = ["watch", "camera", "phone"]


@router.get("/all")
def _() -> list[str]:
    return product
