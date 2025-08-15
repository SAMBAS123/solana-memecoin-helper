import os
import time
import requests
from dotenv import load_dotenv
from typing import Callable, Optional

load_dotenv()
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")


def get_token_overview(token_address: str) -> Optional[dict]:
    url = f"https://public-api.birdeye.so/defi/token_overview?address={token_address}"
    headers = {"X-API-KEY": BIRDEYE_API_KEY or "", "x-chain": "solana"}
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        return resp.json().get("data", {})
    return None


def monitor_liquidity_poll(
    token_address: str,
    threshold_pct: float = 10.0,
    check_interval_sec: int = 60,
    on_alert: Optional[Callable[[dict], None]] = None,
    stop_flag: Optional[Callable[[], bool]] = None,
) -> None:
    peak_liquidity = 0.0
    while True:
        if stop_flag and stop_flag():
            return

        info = get_token_overview(token_address)
        if info is not None:
            current_liquidity = float(info.get("liquidity", 0.0))
            if current_liquidity > peak_liquidity:
                peak_liquidity = current_liquidity

            if peak_liquidity > 0 and current_liquidity < peak_liquidity * (1 - threshold_pct / 100.0):
                payload = {
                    "token": token_address,
                    "current_liquidity": current_liquidity,
                    "peak_liquidity": peak_liquidity,
                    "threshold_pct": threshold_pct,
                }
                if on_alert:
                    on_alert(payload)

        time.sleep(check_interval_sec)
