from fastapi import HTTPException 
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from database import SessionLocal
from actions.util.jwtHelper import JwtHelper 


class JWTMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # paths to exclude
        excluded_paths = {"/openapi.json", "/docs", "/user/login", "/user/create-account", "/user/refresh-token"}

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