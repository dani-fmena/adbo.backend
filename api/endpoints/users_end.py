from typing import Union
from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from models.user import User
from api.utils.extensions import dt_query_params
from api.utils.definition_types import DQueryData
from api.utils.definition_perms import PG_USERS
from services.users_svc import UsersSvc
from services.auth.authorization_svc import AuthorizationSvc
from api.utils.definition_data import SDES

router = APIRouter()


@router.get("/", responses = {status.HTTP_204_NO_CONTENT: SDES.NO_CONTENT}, dependencies = [Depends(AuthorizationSvc(PG_USERS.LIST))])
async def get_users(response: Response, service: UsersSvc = Depends(), qd: DQueryData = Depends(dt_query_params)):       # qd means query data
    users = await service.get_parametrized(qd)
    if len(users) > 0: return users

    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/count", description = 'Get the total documents in the collection', dependencies = [Depends(AuthorizationSvc(PG_USERS.LIST))])
async def get_count(service: UsersSvc = Depends()):
    return await service.get_count()


@router.get("/{user_id}",
            response_model = User,
            dependencies = [Depends(AuthorizationSvc(PG_USERS.VIEW))],
            responses = {status.HTTP_400_BAD_REQUEST: SDES.BAD_REQUEST},
            )
async def get_user(user_id: str, service: UsersSvc = Depends()):
    return await service.get_by_id(user_id)


@router.get("/username/{username}",
            response_model = User,
            dependencies = [Depends(AuthorizationSvc(PG_USERS.VIEW))],
            responses = {status.HTTP_400_BAD_REQUEST: SDES.BAD_REQUEST},
            )
async def get_user_by_username(username: str, service: UsersSvc = Depends()):
    return await service.get_by_username(username)
