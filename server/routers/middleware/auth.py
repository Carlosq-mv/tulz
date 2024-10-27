from fastapi import Request, HTTPException, status, Depends, status
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
import jwt, os
from datetime import timedelta, datetime, timezone

from schemas.user_schema import UserResponse
from schemas.token_schema import TokenData
from models.user import User
from dependencies import get_db

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JWTMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # paths to exclude
        excluded_paths = {"/openapi.json", "/docs", "/user/login", "/user/create-account"}

        # check if the request path is excluded
        if request.url.path in excluded_paths:
            return await call_next(request)

        try:

            verify_token(request)
            response = await call_next(request)
        except HTTPException as e:
            return JSONResponse(content={"detail":e.detail}, status_code=e.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
        return response 


def verify_token(request: Request):
    token = get_token_from_cookie(request)
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if token is None:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # store user info into the request state
        username_ = payload.get("username")
        email_ = payload.get("email")
        
        if username_ is None or email_ is None:
            raise credentials_exception 

        token_data = TokenData(
            access_token=token,     # The JWT itself can be treated as the access token
            token_type="bearer",    # Define token type
            username=username_,
            email=email_
        )

        request.state.token = token_data
        request.state.user = {"username":username_, "email":email_}
    except jwt.InvalidTokenError:
        raise credentials_exception

                
def get_token_from_cookie(request: Request):
    return request.cookies.get("jwt_token")

# TODO: fix database injection outside of fastapi methods to reduce redundant queries
# in "logout" and "current-user" routes
def get_user(email: str, username: str):
    db = get_db()
    user = db.query(User).filter(User.username==username, User.email==email).first()
    if user is None:
        return None
    return UserResponse(
        id=user.id,  # Assuming your User model has an id attribute
        name=user.name,
        username=user.username,
        email=user.email,
        is_logged_in=user.is_logged_in # Or derive this from your user logic
    )

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)       
    to_encode.update({"exp" : expire})
    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
