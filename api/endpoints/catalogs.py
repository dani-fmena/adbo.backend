from fastapi import APIRouter
from typing import List
from models.catalog import Catalog
from services.catalogs_srv import CatalogService

router = APIRouter()


@router.get("/")
async def get_catalogs():
    return await CatalogService.get_all()


@router.get("/{id}", response_model=Catalog)
async def get_catalog(id: int):
    return {"name": "films"}


@router.post("/", response_model=Catalog)
async def create_catalog(catalog_req: Catalog):
    return await CatalogService.create(catalog_req)
