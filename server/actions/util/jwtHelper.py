from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt, os

from models.user import User
from schemas.token_schema import TokenData
from schemas.user_schema import UserResponse


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JwtHelper():
    def __init__(self, db):
        self.db = db

    async def verify_token(self, request: Request):
        token = request.cookies.get("jwt_token")
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
            request.state.user = await self.get_user(email_, username_)
        except jwt.InvalidTokenError:
            raise credentials_exception

    async def get_user(self, email: str, username: str) -> UserResponse:
        user = self.db.query(User).filter(User.username==username, User.email==email).first()

        if user is None:
            return None
        return UserResponse(
            id=user.id,  # Assuming your User model has an id attribute
            name=user.name,
            username=user.username,
            email=user.email,
            is_logged_in=user.is_logged_in # Or derive this from your user logic
        )