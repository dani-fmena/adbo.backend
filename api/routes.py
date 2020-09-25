from fastapi import APIRouter
from api.endpoints import categories, catalogs
from api.utils.definitions import SCODE, SDES, TAGS


adbo_router = APIRouter()

adbo_router.include_router(
    catalogs.router,
    prefix="/catalogs",
    tags=[TAGS.CATALOG],
    responses={SCODE.c404: SDES.NOTFOUND},
)

adbo_router.include_router(
    categories.router,
    prefix="/categories",
    tags=[TAGS.CATEGORY],
    responses={SCODE.c404: SDES.NOTFOUND},
)