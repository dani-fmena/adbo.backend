from fastapi import APIRouter
from utils.definitions import TAGS

router = APIRouter()


@router.get("/catalogs/", tags=[TAGS.CATALOG])
async def get_catalogs():
    return [
        {"name": "films"},
        {"name": "games"}
    ]


@router.get("/catalogs/{id}", tags=[TAGS.CATALOG])
async def get_catalog():
    return {"name": "films"}
