from fastapi import Depends, FastAPI, Header, HTTPException
from .routers import catalogs, categories

app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(
    catalogs.router

)

app.include_router(
    categories.router,
    prefix="/categories",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
