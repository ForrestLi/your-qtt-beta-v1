from fastapi import APIRouter

from app.api.api_v1.endpoints import market

api_router = APIRouter()

# Include all endpoint routers here
api_router.include_router(market.router, prefix="/market", tags=["market"])
