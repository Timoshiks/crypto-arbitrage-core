from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.modules.crypto.router import ws_router
from app.modules.crypto.service import crypto_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    await crypto_service.start()
    yield
    await crypto_service.stop()

app = FastAPI(lifespan = lifespan, title = "Crypto Arbitrage Platform")
app.include_router(ws_router)

    