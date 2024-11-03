from fastapi import APIRouter, Depends
from ..schemas.user import (UserLoginRequest, UserLoginResponse, UserRegisterRequest, UserRegisterResponse,
                            UserProfileResponse)
from ..schemas.base import ErrorResponse, MessageBase
from ..crud.user import register_account_handler, login_account_handler, read_profile_user
from ..models.db import get_session
from sqlmodel import Session
from fastapi_jwt_auth import AuthJWT
from ..utils.auth import denylist

router = APIRouter(
    prefix="/user",
    tags=['user']
)

@router.post("/register",
             responses={
                 400: {"model": ErrorResponse, "description": "Bad Request - Invalid input data"},
                 409: {"model": ErrorResponse, "description": "Conflict - The resource already exists"}
             },
             status_code=201,
             response_model=UserRegisterResponse)
async def register(user: UserRegisterRequest, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    result = register_account_handler(user=user, session=session, auth=auth)
    response = UserRegisterResponse(message="Account has been successfully created",
                                    data=result)
    return response

@router.post("/login",
             responses={401: {"model": ErrorResponse, "description": "Authentication failed - Missing or invalid credentials"}},
             status_code=200,
             response_model=UserLoginResponse)
async def login(user: UserLoginRequest, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    result = login_account_handler(session=session, auth=auth, user=user)
    response = UserLoginResponse(message="Login has been successful",
                                 data=result)
    return response

@router.get("/logout",
            status_code=200,
            responses={401: {"model": ErrorResponse, "description": "Unauthorized - Please provide valid authentication credentials."}},
            response_model=MessageBase)
async def logout(auth: AuthJWT = Depends()):
    auth.jwt_required()
    jti_acces_token = auth.get_raw_jwt()['jti']
    denylist.add(jti_acces_token)
    return MessageBase(message="Account has been successfully logged out")

@router.get("/me",
            status_code=200,
            responses={401: {"model": ErrorResponse, "description": "Unauthorized - Please provide valid authentication credentials."},
                       422: {"model": ErrorResponse, "description":"Unprocessable Entity - The request contains semantic errors or validation issues."}},
            response_model=UserProfileResponse)
async def me(auth: AuthJWT = Depends(), session: Session = Depends(get_session)):
    auth.jwt_required()
    response = read_profile_user(session=session, auth=auth)
    return response