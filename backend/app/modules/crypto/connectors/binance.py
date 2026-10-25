import json
from .hh import BaseCryptoWS

class BinanceWS(BaseCryptoWS):
    url = "wss://stream.binance.com:9443/stream"

    def exchange_parse(self, raw_data):
        try:
            payload = json.loads(raw_data)
            if "data" in payload:
                data = payload["data"]
                return (
                    "binance",
                    data["s"],
                    float(data["b"]),
                    float(data["B"]),
                    float(data["a"]),
                    float(data["A"])
                )
        except (KeyError, ValueError, json.JSONDecodeError):
            pass

        return None

    def build_subscribe_payload(self) -> dict:
        return {
            "method": "SUBSCRIBE",
            "params" : [f"{s.lower()}@bookTicker" for s in self.symbols],
            "id": 1,
        }
        
    