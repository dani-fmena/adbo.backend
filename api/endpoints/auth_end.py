from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth.authentication_svc import AuthenticationSvc
from models.auth import AccessToken
from api.utils.definition_data import SDES

router = APIRouter()


@router.post("/token", description = 'Get the authorization token', response_model = AccessToken, responses = {status.HTTP_401_UNAUTHORIZED: SDES.UNAUTHORIZED})
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), service: AuthenticationSvc = Depends()):
    auth_user = await service.authenticate_user(form_data.username, form_data.password)

    if not auth_user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    return await service.create_token(auth_user.username)
