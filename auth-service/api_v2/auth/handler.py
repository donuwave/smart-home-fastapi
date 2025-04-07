from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


from .dependency import get_auth_service
from .schema import AuthResponse, RegistrationRequest, LoginRequest
from .service import AuthService

router = APIRouter(tags=["auth"])
http_bearer = HTTPBearer()


@router.post("/login", response_model=AuthResponse)
async def login(
    login_request: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.login(login_request=login_request)


@router.post("/registration", response_model=AuthResponse)
async def registration(
    register_request: RegistrationRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.registration(register_request=register_request)


@router.post(
    "/refresh", response_model=AuthResponse, dependencies=[Depends(http_bearer)]
)
async def refresh(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await auth_service.refresh(credentials=credentials)


@router.post("/logout", dependencies=[Depends(http_bearer)])
async def logout(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await auth_service.logout(credentials=credentials)
