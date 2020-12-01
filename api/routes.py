from fastapi import APIRouter, status
from api.endpoints import categories_end, catalogs_end, dev_end
from api.utils.definitions import SDES, TAGS


adbo_router = APIRouter()

adbo_router.include_router(
    catalogs_end.router,
    prefix="/catalogs",
    tags=[TAGS.CATALOG],
    responses={
        status.HTTP_404_NOT_FOUND: SDES.NOTFOUND,
        status.HTTP_403_FORBIDDEN: SDES.FORBIDDEN,
    },
)

adbo_router.include_router(
    categories_end.router,
    prefix="/categories",
    tags=[TAGS.CATEGORY],
    responses={
        status.HTTP_404_NOT_FOUND: SDES.NOTFOUND,
        status.HTTP_403_FORBIDDEN: SDES.FORBIDDEN,
    },
)

adbo_router.include_router(
    dev_end.router,
    prefix="/dev",
    tags=[TAGS.DEV],
    responses={
        status.HTTP_404_NOT_FOUND: SDES.NOTFOUND,
    },
)
