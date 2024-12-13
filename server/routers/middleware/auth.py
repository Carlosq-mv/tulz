from fastapi import HTTPException 
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt as pyjwt
from datetime import timedelta, datetime, timezone

from database import SessionLocal
from actions.util.jwtHelper import JwtHelper, SECRET_KEY, ALGORITHM


class JWTMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # paths to exclude
        excluded_paths = {"/openapi.json", "/docs", "/user/login", "/user/create-account"}

        # check if the request path is excluded
        if request.url.path in excluded_paths:
            return await call_next(request)
        db = SessionLocal()
        jwtHelper = JwtHelper(db)
        try:

            await jwtHelper.verify_token(request)
            response = await call_next(request)
        except HTTPException as e:
            return JSONResponse(content={"detail":e.detail}, status_code=e.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
        finally:
            db.close() 
        return response 


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)       
    to_encode.update({"exp" : expire})
    encoded_jwt= pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt