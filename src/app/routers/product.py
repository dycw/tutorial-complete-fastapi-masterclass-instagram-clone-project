from typing import Any
from typing import Optional

from dycw_utilities.fastapi import APIRouter
from fastapi import Cookie
from fastapi import Header
from fastapi import Response
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_404_NOT_FOUND


router = APIRouter(prefix="/product", tags=["product"])


products = ["watch", "camera", "phone"]


@router.get("/all")
def _() -> Response:
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response


@router.get("/withheader")
def _(
    *,
    response: Response,
    custom_header: Optional[str] = Header(None),
    custom_headers: Optional[list[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
) -> dict[str, Any]:
    if custom_headers is not None:
        response.headers["custom_response_header"] = ",".join(custom_headers)
    return {
        "data": products,
        "custom_header": custom_header,
        "my_cookie": test_cookie,
    }


@router.get(
    "/{id}",
    responses={
        HTTP_200_OK: {
            "content": {"text/html": {"example": "<div>Product</div>"}},
            "description": "Returns the HTML for an object",
        },
        HTTP_404_NOT_FOUND: {
            "content": {"text/plain": {"example": "Product not found"}},
            "description": "A cleartext error message",
        },
    },
)
def _(*, id: int) -> Response:
    try:
        product = products[id]
    except IndexError:
        content = "Product not available"
        return PlainTextResponse(
            content=content,
            status_code=HTTP_404_NOT_FOUND,
            media_type="text/plain",
        )
    else:
        content = f"""
        <html>
          <head>
            <style>
            .product {{
              width: 500px;
              height: 30px;
              border: 2px inset green;
              background-color: lightblue;
              text-align: center;
            }}
            </style>
          </head>

          <div class="product">
            {product}
          </div>
        </html>
        """
        return HTMLResponse(content=content, media_type="text/html")
