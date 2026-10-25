import time
from typing import TypedDict
from collections import defaultdict

class TickerData(TypedDict):
    bid: float
    bid_size: float
    ask: float
    ask_size: float
    ts: float

class CryptoManager:
    def __init__(self):
        self._crypto: dict[str, dict[str, TickerData]] = defaultdict(dict)
    def update_rate(self, parse_data : tuple[str, str, float, float, float, float]) -> None:
        pair, exchange, bid, bid_size, ask, ask_size = parse_data
        
        if pair not in self._crypto:
            self._crypto[pair] = {}

        self._crypto[pair][exchange] = {
            "bid": bid,
            "bid_size": bid_size,
            "ask": ask,
            "ask_size": ask_size,
            "ts": time.time(),
        }

    def get_all_rates(self) -> dict[str, dict[str, TickerData]]:
        return self._crypto

crypto_manager = CryptoManager()