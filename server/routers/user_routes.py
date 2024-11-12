from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import timedelta

from dependencies import get_user_services
from schemas.user_schema import UserResponse, UserCreate, UserLogin
from models.user import User
from routers.middleware.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MIN
from actions.services.userServices import UserServices


u_routes = APIRouter()


# create account API route
@u_routes.post("/create-account", response_model=UserResponse)
async def create_account(user: UserCreate, user_services: UserServices = Depends(get_user_services)) -> User:
    created_user = await user_services.add_user(user)
    return created_user


# login API route
@u_routes.post("/login", response_model=UserResponse)
async def login(user: UserLogin, response: Response, user_services: UserServices = Depends(get_user_services)) -> User:

    expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    jwt_token = create_access_token({"username":user.username, "email":user.email}, expires_delta=expires_time)
    response.set_cookie(key="jwt_token", value=jwt_token, httponly=True, samesite="None", secure=True) 

    return await user_services.login_user(user)


# # logout route
@u_routes.post("/logout", response_model=UserResponse)
async def logout(response: Response, request: Request, user_services: UserServices = Depends(get_user_services)):
    username =  request.state.user.get("username")
    email = request.state.user.get("email")

    response.delete_cookie("jwt_token")
    return await user_services.logout_user(username, email)


# # get current auth user API route
@u_routes.get("/current-user", response_model=UserResponse) 
async def current_user(request: Request, user_services: UserServices = Depends(get_user_services)):
    username =  request.state.user.get("username")
    email = request.state.user.get("email")

    return await user_services.get_current_user(username, email)


# # get all of the users
# @u_routes.get("/all-users",response_model=list[UserResponse]) 
# def get_all_users(db: Session = Depends(get_db)) -> list[UserResponse]:
#     users = db.query(User).all()
#     return [UserResponse.model_validate(u) for u in users]