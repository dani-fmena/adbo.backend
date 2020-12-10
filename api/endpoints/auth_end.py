from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_srv import AuthServices
from models.auth import AccessToken

router = APIRouter()


@router.post("/token", description = 'Get the authorization token', response_model = AccessToken)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), service: AuthServices = Depends()):
    auth_user = await service.authenticate_user(form_data.username, form_data.password)

    if not auth_user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    return await service.mk_access_token(auth_user.username)
