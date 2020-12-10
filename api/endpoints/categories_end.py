from fastapi import APIRouter
from models_vm.vmCategory import CategoryIn

router = APIRouter()


@router.get("/")
async def get_categories():
    return [
        {'name': 'films'},
        {'name': 'games'}
    ]


@router.get("/{id}", response_model=CategoryIn)
async def get_category(id: int):
    return {'name': 'films'}



