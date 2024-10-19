from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

allowed_url = os.getenv('ALLOWED_URL')
if not allowed_url:
    raise ValueError('ALLOWED_URL env variable not set')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_url,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
