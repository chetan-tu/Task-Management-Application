from fastapi import FastAPI

from .endpoint import router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#FastAPI instance
app = FastAPI()

origins = ["*"] # allowing access to all domain for simplicty but can be restricted as needed.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)