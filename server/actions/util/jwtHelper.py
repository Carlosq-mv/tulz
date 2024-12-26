from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt, os

from models.user import User
from schemas.token_schema import TokenData


SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JwtHelper():
    def __init__(self, db):
        self.db = db   
        self.credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"}
            )

    async def verify_token(self, request: Request):
        token = request.cookies.get("jwt_token")

        if token is None:
            raise self.credentials_exception
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if payload.get("token_type") != "access":
                raise HTTPException(status_code=403, detail="Invalid token type")

            # store user info into the request state
            user_id = payload.get("user_id")
            
            if user_id is None:
                raise self.credentials_exception 

            token_data = TokenData(
                access_token=token,     # The JWT itself can be treated as the access token
                token_type=payload.get("token_type"),    # Define token type
                id=user_id
            )

            request.state.token = token_data
            request.state.user = await self.get_user(user_id)
        except jwt.InvalidTokenError:
            raise self.credentials_exception


    async def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id==user_id).first()


    @staticmethod 
    async def verify_refresh_token(refresh_token: str):
        credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if refresh_token is None:
            raise self.credentials_exception

        try:
            payload = jwt.decode(refresh_token, REFRESH_KEY, algorithms=ALGORITHM)
            if payload.get("token_type") != "refresh":
                raise HTTPException(status_code=403, detail="Invalid token type")

            return payload
        except jwt.InvalidTokenError:
            raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
  

    @staticmethod
    async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)       
        to_encode.update({"exp" : expire, "token_type" : "access"})
        encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    @staticmethod
    async def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"exp" : expire, "token_type" : "refresh"})
        encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, algorithm=ALGORITHM)
        return encoded_jwt