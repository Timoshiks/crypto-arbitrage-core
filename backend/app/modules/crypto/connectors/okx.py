import json
from .hh import BaseCryptoWS

class OkxWS(BaseCryptoWS):
    url = "wss://ws.okx.com:8443/ws/v5/public"

    def get_ping_config(self) -> tuple[str, int] | None:
        return ('{"op": "ping"}', 20)
    
    def exchange_parse(self, raw_data):
        try:
            payload = json.loads(raw_data)
            if "data" in payload and payload["data"]:
                data = payload["data"][0]
                instId = payload["arg"]["instId"]
                return (
                    "okx",
                    instId.replace("-", ""),
                    float(data["bids"][0][0]),
                    float(data["bids"][0][1]),
                    float(data["asks"][0][0]),
                    float(data["asks"][0][1])
                )
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            pass

        return None

    def build_subscribe_payload(self) -> dict:
        args = [
            {"channel": "bbo-tbt", "instId" : s} 
            for s in self.symbols
        ]
        return {
            "op": "subscribe",
            "args" : args,
        }
        
    