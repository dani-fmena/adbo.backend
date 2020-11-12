from fastapi import APIRouter, Depends, Response, status
from models.catalog import Catalog
from services.catalogs_srv import CatalogService
from api.utils.definitions import SDES

router = APIRouter()


@router.get("/", responses={status.HTTP_204_NO_CONTENT: SDES.NOCONTENT})
async def get_catalogs(response: Response, service: CatalogService = Depends()):
    catalogs = await service.get_all()
    if len(catalogs) > 1: return catalogs

    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/{catalog_id}", response_model=Catalog, responses={status.HTTP_400_BAD_REQUEST: SDES.BADREQUEST})
async def get_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.get_catalog(catalog_id)


@router.post("/", response_model=Catalog, status_code = status.HTTP_201_CREATED)
async def create_catalog(catalog_req: Catalog, service: CatalogService = Depends()):
    return await service.create(catalog_req)


@router.post("/enable/{catalog_id}", description = "Enable Catalog", responses={status.HTTP_417_EXPECTATION_FAILED: SDES.EXPECTATIONFAIL})
async def enable_catalog(catalog_id: str, response: Response, service: CatalogService = Depends()):
    if await service.set_status(catalog_id, True): return
    else:
        response.status_code = status.HTTP_417_EXPECTATION_FAILED
        return


@router.post("/disable/{catalog_id}", description = "Disable Catalog", responses={status.HTTP_417_EXPECTATION_FAILED: SDES.EXPECTATIONFAIL})
async def disable_catalog(catalog_id: str, response: Response, service: CatalogService = Depends()):
    if await service.set_status(catalog_id, False): return
    else:
        response.status_code = status.HTTP_417_EXPECTATION_FAILED
        return


@router.put("/", response_model=Catalog)
async def update_catalog(catalog_req: Catalog, service: CatalogService = Depends()):
    return await service.update(catalog_req)


@router.delete("/{catalog_id}", response_model=Catalog, responses={status.HTTP_400_BAD_REQUEST: SDES.BADREQUEST})
async def delete_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.delete(catalog_id)
