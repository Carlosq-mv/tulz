from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

from routers.user_api import u_api
from routers.websockets import wb_routes
from routers.friendship_api import f_api
from database import Base, engine
from routers.middleware.auth import JWTMiddleWare

Base.metadata.create_all(bind=engine)

app = FastAPI()

allowed_url = os.getenv("ALLOWED_URL")
if not allowed_url:
    raise ValueError('ALLOWED_URL env variable not set')

allowed_origins = [allowed_url, 'http://localhost:3000']  # Wrap the URL in a list

app.add_middleware(JWTMiddleWare)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(u_api, prefix="/user", tags=["Users"])
app.include_router(wb_routes, tags=["Websocket"])
app.include_router(f_api, prefix="/friend", tags=["Friends"])