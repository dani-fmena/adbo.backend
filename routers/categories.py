from fastapi import APIRouter
from utils.definitions import TAGS

router = APIRouter()


@router.get("/")
async def get_categories():
    return [
        {"name": "films"},
        {"name": "games"}
    ]


@router.get("/{id}")
async def get_category():
    return {"name": "films"}
