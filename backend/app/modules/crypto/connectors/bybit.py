import json
from .hh import BaseCryptoWS

class BybitWS(BaseCryptoWS):
    url = "wss://stream.bybit.com/v5/public/spot"

    def get_ping_config(self) -> tuple[str, int] | None:
        return ('{"op": "ping"}', 20)
    
    def exchange_parse(self, raw_data: str) -> tuple[str, str, float, float, float, float] | None:
        try:
            payload = json.loads(raw_data)
            if "data" in payload and isinstance(payload["data"], dict):
                data = payload["data"]

                bids = data.get("b", [])
                asks = data.get("a", [])
                if bids and asks:
                    return (
                        "bybit",
                        data["s"],
                        float(bids[0][0]),
                        float(bids[0][1]),
                        float(asks[0][0]),
                        float(asks[0][1]),
                    )
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            pass

        return None

    def build_subscribe_payload(self) -> dict:
        args = [
            f"orderbook.1.{s.upper()}"
            for s in self.symbols
        ]
        return {
            "op": "subscribe",
            "args" : args,
        }
        
    