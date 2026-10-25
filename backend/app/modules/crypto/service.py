import asyncio
from .connectors.binance import BinanceWS
from .connectors.bybit import BybitWS
from .connectors.okx import OkxWS

class CryptoService:
    def __init__(self):
        self.tasks: list[asyncio.Task] = []

    async def start(self):
        symbols = ["BTCUSDT", "ETHUSDT"]

        exchanges = [
            BinanceWS(symbols=symbols),
            BybitWS(symbols=symbols),
            OkxWS(symbols=["BTC-USDT", "ETH-USDT"]),
        ]
        self.tasks = [
            asyncio.create_task(ws.listen_exchange()) for ws in exchanges
        ]
    async def stop(self):
        for task in self.tasks:
            task.cancel()
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)

crypto_service = CryptoService()
