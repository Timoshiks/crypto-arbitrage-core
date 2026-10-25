import asyncio
import websockets
import json
import random
from abc import ABC, abstractmethod
from app.modules.crypto.manager import crypto_manager

class BaseCryptoWS(ABC):
    url: str

    def __init__(self, symbols: list[str]):
        self.symbols = symbols
        self.subscribe_payload = self.build_subscribe_payload()

    @abstractmethod
    def build_subscribe_payload(self) -> dict:
        pass

    def get_ping_config(self) -> tuple[str, int] | None:
        return None
    
    @abstractmethod
    def exchange_parse(self, data: str) -> tuple[str, str, float, float, float, float]:
        pass

    async def _ping_loop(self, ws, ping_config: tuple[str, int]):
        ping_payload, ping_interval = ping_config
        try:
            while True:
                await asyncio.sleep(ping_interval)
                await ws.send(ping_payload)
        except asyncio.CancelledError:
            pass
    
    async def listen_exchange(self):
        delay = 1.0 + random.uniform(0.0, 0.3)
        max_delay = 30
        while True:
            try:
                async with websockets.connect(self.url) as ws:
                    await ws.send(json.dumps(self.subscribe_payload))
                    ping_config= self.get_ping_config()
                    ping_task = None
                    if ping_config is not None:
                        ping_task = asyncio.create_task(self._ping_loop(ws, ping_config))
                    try:
                        while True:
                            raw_data = await ws.recv()
                            delay = 1.0 + random.uniform(0.0, 0.3)
                            parsed = self.exchange_parse(raw_data)
                            if parsed:
                                crypto_manager.update_rate(parsed)
                    finally:
                        if ping_task and not ping_task.done():
                            ping_task.cancel()
                            await asyncio.gather(
                                ping_task, return_exceptions=True
                            )

            except(
                websockets.ConnectionClosed,
                asyncio.TimeoutError,
                OSError,
            ) as err:
                print(f"Ошибка: {err}")
                await asyncio.sleep(delay)
                delay = min(delay * 2 + random.uniform(0.0, 0.3), max_delay)

