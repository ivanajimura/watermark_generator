from fastapi import APIRouter

from backend.apis.v1 import route_watermark


api_router = APIRouter()

api_router.include_router(router=route_watermark.router, prefix='', tags = [''])