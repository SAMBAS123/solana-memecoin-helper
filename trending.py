import requests
from dotenv import load_dotenv
import os
from cachetools import TTLCache

load_dotenv()

GMGN_API_HOST = os.getenv("GMGN_API_HOST", "https://gmgn.ai")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", 5))

cache = TTLCache(maxsize=100, ttl=300)

def get_trending_coins(limit=10):
    key = ('trending_coins', limit)
    if key in cache:
        return cache[key]
    url = f"{GMGN_API_HOST}/defi/quotation/v1/tokens/trending/sol?direction=desc&limit={limit}&orderby=txs_5m"
    try:
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()['data']
        result = [{"address": d['address'], "name": d['symbol']} for d in data]
        cache[key] = result
        return result
    except Exception as e:
        return {"error": str(e)}
