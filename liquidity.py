import requests
from dotenv import load_dotenv
import os
from cachetools import TTLCache
import numpy as np
from scipy.signal import find_peaks

load_dotenv()

GMGN_API_HOST = os.getenv("GMGN_API_HOST", "https://gmgn.ai")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", 5))

cache = TTLCache(maxsize=100, ttl=300)  # 5 min TTL

def get_liquidity(token):
    """Gets liquidity info from GMGN API, with caching."""
    key = ('liquidity', token)
    if key in cache:
        return cache[key]
    url = f"{GMGN_API_HOST}/defi/quotation/v1/tokens/sol/{token}"
    try:
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()['data']
        result = {
            "liquidity_usd": data.get('liquidity_usd', 0),
            "liquidity_change_5m": data.get('liquidity_change_5m', 0)
        }
        cache[key] = result
        return result
    except Exception as e:
        return {"error": str(e)}

def liq_ta(token):
    """Liquidity TA with scipy peaks on mocked history."""
    ohlc = [get_liquidity(token) for _ in range(10)]  # Mock 10 intervals
    liq_levels = np.array([d["liquidity_usd"] if 'liquidity_usd' in d else 0 for d in ohlc])
    resistance, _ = find_peaks(liq_levels, distance=3)
    support, _ = find_peaks(-liq_levels, distance=3)
    alpha = "Buy on support hold" if support.size else "Watch resistance break"
    return {"support": liq_levels[support].mean() if support.size else 0, "resistance": liq_levels[resistance].mean() if resistance.size else 0, "alpha": alpha}
