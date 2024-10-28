from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import timedelta

from dependencies import get_db
from schemas.user_schema import UserResponse, UserCreate, UserBase, UserLogin
from schemas.token_schema import TokenData
from models.user import User
from routers.middleware.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MIN


u_routes = APIRouter()


# create account API route
@u_routes.post("/create-account", response_model=UserResponse)
def create_account(user: UserCreate, db: Session = Depends(get_db)) -> User:
    # check if all fields are not empty
    if not user.username or not user.email or not user.password or not user.name:
        raise HTTPException(status_code=400, detail="All fields are required")

    # check if the user inputted email or username already exists
    existing_user = db.query(User).filter(
        or_ (
            User.email == user.email,
            User.username == user.username
        )
    ).first()

    # if it does exists throw HTTP error
    if existing_user:
        raise HTTPException(status_code=400, detail="Email and/or username already registered")
    return create_user(db, user) 


# login API route
@u_routes.post("/login", response_model=UserResponse)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)) -> User:
    user_ = db.query(User).filter(User.email == user.email, User.username == user.username).first()
    if user_ is None:
        raise HTTPException(status_code=404, detail="User does exists")
    # check if password is correct
    if not user_.check_password(user.password):
       raise HTTPException(status_code=404, detail="password is not correct") 
 
    # set jwt token in cookie
    expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    jwt_token = create_access_token({"username":user_.username, "email":user_.email}, expires_delta=expires_time)
    response.set_cookie(key="jwt_token", value=jwt_token, httponly=True, samesite="None", secure=True) 
    user_.is_logged_in = True
    db.commit()
    
    return user_


# logout route
@u_routes.post("/logout", response_model=UserResponse)
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    username =  request.state.user.get("username")
    email = request.state.user.get("email")
    current_user = db.query(User).filter(User.username == username, User.email == email).first()
    current_user.is_logged_in = False
    response.delete_cookie("jwt_token")
    return current_user


# get current auth user API route
@u_routes.get("/current-user", response_model=UserResponse) 
def current_user(request: Request, db: Session = Depends(get_db)):
    username =  request.state.user.get("username")
    email = request.state.user.get("email")
    user = db.query(User).filter(User.username == username, User.email == email).first()
    return user


# get token info
@u_routes.get("/token-data", response_model=TokenData)
def token_data(request: Request):
    return request.state.token










# get a particular user by id
@u_routes.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == id).first()
    return user

# get all of the users
@u_routes.get("/all-users") 
def get_all_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    users = db.query(User).all()
    return [UserResponse.model_validate(u) for u in users]

# helper methods to create a new user
def create_user(db: Session, user: UserCreate) -> User:
    new_user = User(name=user.name, email=user.email, username=user.username)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    return new_user