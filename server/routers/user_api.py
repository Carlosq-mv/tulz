from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response

from dependencies import get_user_services
from schemas.user_schema import UserResponse, UserCreate, UserLogin
from schemas.token_schema import *
from actions.services.userServices import UserServices


u_api = APIRouter()


# create account API route
@u_api.post("/create-account", response_model=UserResponse)
async def create_account(user: UserCreate, user_services: UserServices = Depends(get_user_services)) -> UserResponse:
    created_user = await user_services.add_user(user)
    return created_user


# login API route
@u_api.post("/login", response_model=TokenData)
async def login(user: UserLogin, response: Response, user_services: UserServices = Depends(get_user_services)) -> TokenData:
    # validate user login data
    jwt_access_token, jwt_refresh_token, u = await user_services.login_user(user)

    response.set_cookie(key="jwt_token", value=jwt_access_token, httponly=True, samesite="None", secure=True) 
    response.set_cookie(key="refresh_token", value=jwt_refresh_token, httponly=True, samesite="None", secure=True)

    return TokenData(
        access_token=jwt_access_token,
        token_type="access",
        id=u.id
    )


# refresh token API route
@u_api.post("/refresh-token", response_model=TokenData)
async def refresh_token(request: Request, response: Response, user_services: UserServices = Depends(get_user_services)) -> TokenData:
    refresh_token = request.cookies.get("refresh_token")
    # current_user = request.state.user

    new_access_token, new_refresh_token, user_id = await user_services.handle_refresh_token(refresh_token)

    response.delete_cookie("jwt_token")
    response.delete_cookie("refresh_token")

    response.set_cookie(key="jwt_token", value=new_access_token, httponly=True, samesite="None", secure=True) 
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True, samesite="None", secure=True)


    return TokenData(
        access_token=new_access_token,
        token_type="access",
        id=user_id
    )


# # logout route
@u_api.post("/logout", response_model=UserResponse)
async def logout(response: Response, request: Request) -> UserResponse:
    user = request.state.user

    response.delete_cookie("jwt_token")
    response.delete_cookie("refresh_token")
    
    # clear the user data from the request state
    request.state.user = None
    request.state.token = None

    return user 


# # get current auth user API route
@u_api.get("/current-user", response_model=UserResponse) 
async def current_user(request: Request) -> UserResponse:
    return request.state.user


# # get all of the users
@u_api.get("/all-users",response_model=list[UserResponse]) 
async def get_all_users(user_services: UserServices = Depends(get_user_services)) -> list[UserResponse]:
    users = await user_services.get_all_users() 
    return [UserResponse.model_validate(u) for u in users]