import requests
from dotenv import load_dotenv
import os
from cachetools import TTLCache

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
    """Liquidity technical analysis with change detection."""
    liq = get_liquidity(token)
    if 'error' in liq:
        return liq
    alpha = "Dump risk" if liq["liquidity_change_5m"] < -10 else "Stable liq"
    return {"liquidity_usd": liq["liquidity_usd"], "change_5m": liq["liquidity_change_5m"], "alpha": alpha}
