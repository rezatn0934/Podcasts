from fastapi import APIRouter
from .endpoints import podcasts

api_router = APIRouter()

api_router.include_router(podcasts.api_router, prefix='/v1')
