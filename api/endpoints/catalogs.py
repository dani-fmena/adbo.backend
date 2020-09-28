from fastapi import APIRouter, Depends, Response, status
from models.catalog import Catalog
from services.catalogs_srv import CatalogService
from api.utils.definitions import SDES

router = APIRouter()


@router.get("/", responses={status.HTTP_204_NO_CONTENT: SDES.NOCONTENT})
async def get_catalogs(response: Response, service: CatalogService = Depends()):
    catalogs = await service.get_all()
    if len(catalogs) == 0:
        response.body = catalogs
        response.status_code = status.HTTP_204_NO_CONTENT
    return catalogs


@router.get("/{catalog_id}", response_model=Catalog)
async def get_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.get_catalog(catalog_id)


@router.post("/", response_model=Catalog)
async def create_catalog(catalog_req: Catalog, service: CatalogService = Depends()):
    return await service.create(catalog_req)


@router.put("/", response_model=Catalog)
async def update_catalog(catalog_req: Catalog, service: CatalogService = Depends()):
    return await service.update(catalog_req)


@router.delete("/{catalog_id}", response_model=Catalog)
async def delete_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.delete(catalog_id)

