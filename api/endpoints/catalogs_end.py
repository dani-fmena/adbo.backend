from fastapi import APIRouter, Depends, Response, status
from typing import List, Union
from models.catalog import Catalog
from services.catalogs_srv import CatalogService
from api.utils.definitions import SDES

router = APIRouter()


@router.get("/", responses = {status.HTTP_204_NO_CONTENT: SDES.NO_CONTENT})
async def get_catalogs(response: Response, service: CatalogService = Depends(), skip: Union[int, None] = None, limit: Union[int, None] = None):
    if skip is None: catalogs = await service.get_all()
    else: catalogs = await service.get_catalog_paginated(skip, limit)

    if len(catalogs) > 0: return catalogs

    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/count", description = "Get the total documents in the collection")
async def get_count(service: CatalogService = Depends()):
    return await service.get_count()


@router.get("/{catalog_id}", response_model = Catalog, responses = {status.HTTP_400_BAD_REQUEST: SDES.BAD_REQUEST})
async def get_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.get_catalog(catalog_id)


@router.post("/", response_model = Catalog, status_code = status.HTTP_201_CREATED, responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL
})
async def create_catalog(catalog_req: Catalog, service: CatalogService = Depends()):
    return await service.create(catalog_req)


@router.put("/", response_model = Catalog, responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
    status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY,
})
async def update_catalog(catalog_req: Catalog, service: CatalogService = Depends()):
    return await service.update(catalog_req)


@router.delete("/{catalog_id}", response_model = Catalog, responses = {
    status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL
})
async def delete_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.delete(catalog_id)


@router.post("/enable/{catalog_id}", description = "Enable Catalog", responses = {
    status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
    status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY,
})
async def enable_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.set_status(catalog_id, True)


@router.post("/disable/{catalog_id}", description = "Disable Catalog", responses = {
    status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
    status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY,
})
async def disable_catalog(catalog_id: str, service: CatalogService = Depends()):
    return await service.set_status(catalog_id, False)


@router.post("/bulk/enable", description = "Bulks ops to enable certain amount of catalogs", responses = {
    status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
    status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY,
})
async def enable_bulk_catalogs(catalog_ids: List[str], service: CatalogService = Depends()):
    return await service.bulk_set_status(catalog_ids, True)


@router.post("/bulk/disable", description = "Bulks ops to disable certain amount of catalogs", responses = {
    status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
    status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY
})
async def bulk_disable_catalogs(catalog_ids: List[str], service: CatalogService = Depends()):
    return await service.bulk_set_status(catalog_ids, False)


@router.post("/bulk/remove", description = "Bulks ops to remove certain amount of catalogs", responses = {
    status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
    status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL
})
async def bulk_remove_catalogs(catalog_ids: List[str], service: CatalogService = Depends()):
    return await service.bulk_remove(catalog_ids)

