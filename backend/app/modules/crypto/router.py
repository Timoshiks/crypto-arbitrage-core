from fastapi import APIRouter
from .manager import crypto_manager

ws_router = APIRouter(prefix = "/ws", tags = ["WS"])

@ws_router.get("/")
async def get_rates():
    rates = crypto_manager.get_all_rates()
    return{"rates": rates}