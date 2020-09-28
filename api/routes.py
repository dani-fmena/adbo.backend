from fastapi import APIRouter, status
from api.endpoints import categories, catalogs
from api.utils.definitions import SDES, TAGS


adbo_router = APIRouter()

adbo_router.include_router(
    catalogs.router,
    prefix="/catalogs",
    tags=[TAGS.CATALOG],
    responses={status.HTTP_404_NOT_FOUND: SDES.NOTFOUND},
)

adbo_router.include_router(
    categories.router,
    prefix="/categories",
    tags=[TAGS.CATEGORY],
    responses={status.HTTP_404_NOT_FOUND: SDES.NOTFOUND},
)
