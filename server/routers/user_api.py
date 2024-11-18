from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from datetime import timedelta

from dependencies import get_user_services
from schemas.user_schema import UserResponse, UserCreate, UserLogin
from models.user import User
from routers.middleware.auth import create_access_token 
from actions.util.jwtHelper import ACCESS_TOKEN_EXPIRE_MIN
from actions.services.userServices import UserServices


u_api = APIRouter()


# create account API route
@u_api.post("/create-account", response_model=UserResponse)
async def create_account(user: UserCreate, user_services: UserServices = Depends(get_user_services)) -> UserResponse:
    created_user = await user_services.add_user(user)
    return created_user


# login API route
@u_api.post("/login", response_model=UserResponse)
async def login(user: UserLogin, response: Response, user_services: UserServices = Depends(get_user_services)) -> UserResponse:

    expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    jwt_token = create_access_token({"username":user.username, "email":user.email}, expires_delta=expires_time)
    response.set_cookie(key="jwt_token", value=jwt_token, httponly=True, samesite="None", secure=True) 

    return await user_services.login_user(user)


# # logout route
@u_api.post("/logout", response_model=UserResponse)
async def logout(response: Response, request: Request, user_services: UserServices = Depends(get_user_services)) -> UserResponse:
    user = request.state.user

    response.delete_cookie("jwt_token")
    return await user_services.logout_user(user.username, user.email)


# # get current auth user API route
@u_api.get("/current-user", response_model=UserResponse) 
async def current_user(request: Request) -> UserResponse:
    return request.state.user


# # get all of the users
@u_api.get("/all-users",response_model=list[UserResponse]) 
async def get_all_users(user_services: UserServices = Depends(get_user_services)) -> list[UserResponse]:
    users = await user_services.get_all_users() 
    return [UserResponse.model_validate(u) for u in users]