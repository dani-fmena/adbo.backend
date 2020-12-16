from fastapi import APIRouter, Response, status
from typing import List
from fastapi.params import Depends
from models.catalog import Catalog
from api.utils.extensions import dt_query_params
from api.utils.definition_types import DQueryData
from api.utils.definition_perms import PG_CATALOG
from services.catalogs_svc import CatalogSvc
from services.auth.authorization_svc import AuthorizationSvc
from api.utils.definition_data import SDES

router = APIRouter()


@router.get("/",
            responses = {status.HTTP_204_NO_CONTENT: SDES.NO_CONTENT},
            dependencies = [Depends(AuthorizationSvc(PG_CATALOG.LIST))],
            )
async def get_catalogs(response: Response, service: CatalogSvc = Depends(), qd: DQueryData = Depends(dt_query_params)):       # qd means query data
    catalogs = await service.get_parametrized(qd)
    if len(catalogs) > 0: return catalogs

    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/count",
            description = 'Get the total documents in the collection',
            dependencies = [Depends(AuthorizationSvc(PG_CATALOG.LIST))],
            )
async def get_count(service: CatalogSvc = Depends()):
    return await service.get_count()


@router.get("/{catalog_id}",
            response_model = Catalog,
            dependencies = [Depends(AuthorizationSvc(PG_CATALOG.VIEW))],
            responses = {status.HTTP_400_BAD_REQUEST: SDES.BAD_REQUEST},
            )
async def get_catalog(catalog_id: str, service: CatalogSvc = Depends()):
    return await service.get_catalog(catalog_id)


@router.post("/",
             response_model = Catalog,
             status_code = status.HTTP_201_CREATED,
             dependencies = [Depends(AuthorizationSvc(PG_CATALOG.CREATE))],
             responses = {status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL}
             )
async def create_catalog(catalog_req: Catalog, service: CatalogSvc = Depends()):
    return await service.create(catalog_req)


@router.put("/",
            response_model = Catalog,
            dependencies = [Depends(AuthorizationSvc(PG_CATALOG.EDIT))],
            responses = {
                status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
                status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY
            })
async def update_catalog(catalog_req: Catalog, service: CatalogSvc = Depends()):
    return await service.update(catalog_req)


@router.delete("/{catalog_id}",
               response_model = Catalog,
               dependencies = [Depends(AuthorizationSvc(PG_CATALOG.DELETE))],
               responses = {
                   status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
                   status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL
               })
async def delete_catalog(catalog_id: str, service: CatalogSvc = Depends()):
    return await service.delete(catalog_id)


@router.post("/enable/{catalog_id}",
             description = "Enable Catalog",
             dependencies = [Depends(AuthorizationSvc(PG_CATALOG.EDIT))],
             responses = {
                 status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
                 status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
                 status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY
             })
async def enable_catalog(catalog_id: str, service: CatalogSvc = Depends()):
    return await service.set_status(catalog_id, True)


@router.post("/disable/{catalog_id}",
             description = "Disable Catalog",
             dependencies = [Depends(AuthorizationSvc(PG_CATALOG.EDIT))],
             responses = {
                 status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
                 status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
                 status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY,
             })
async def disable_catalog(catalog_id: str, service: CatalogSvc = Depends()):
    return await service.set_status(catalog_id, False)


@router.post("/bulk/enable",
             description = "Bulks ops to enable certain amount of catalogs",
             dependencies = [Depends(AuthorizationSvc(PG_CATALOG.EDIT))],
             responses = {
                 status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
                 status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
                 status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY,
             })
async def enable_bulk_catalogs(catalog_ids: List[str], service: CatalogSvc = Depends()):
    return await service.bulk_set_status(catalog_ids, True)


@router.post("/bulk/disable",
             description = "Bulks ops to disable certain amount of catalogs",
             dependencies = [Depends(AuthorizationSvc(PG_CATALOG.EDIT))],
             responses = {
                 status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
                 status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL,
                 status.HTTP_417_EXPECTATION_FAILED:    SDES.DAL_FAIL_EMPTY
             })
async def bulk_disable_catalogs(catalog_ids: List[str], service: CatalogSvc = Depends()):
    return await service.bulk_set_status(catalog_ids, False)


@router.post("/bulk/remove",
             description = "Bulks ops to remove certain amount of catalogs",
             dependencies = [Depends(AuthorizationSvc(PG_CATALOG.DELETE))],
             responses = {
                 status.HTTP_400_BAD_REQUEST:           SDES.BAD_REQUEST,
                 status.HTTP_500_INTERNAL_SERVER_ERROR: SDES.DAL_FAIL
             })
async def bulk_remove_catalogs(catalog_ids: List[str], service: CatalogSvc = Depends()):
    return await service.bulk_remove(catalog_ids)
