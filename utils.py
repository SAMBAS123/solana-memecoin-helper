import requests
from cachetools import TTLCache
from dotenv import load_dotenv
import os

load_dotenv()

GMGN_API_HOST = os.getenv("GMGN_API_HOST", "https://gmgn.ai")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", 5))

cache = TTLCache(maxsize=100, ttl=300)  # 5 min TTL

def get_swap_route(input_token='So11111111111111111111111111111111111111112', output_token=None, amount_lamports=100000000, from_address=None, slippage=0.5, anti_mev=True):
    """Query route for liq/bundle inference; flag risks for <10k MC coins."""
    if from_address is None:
        from_address = os.getenv("WALLET_ADDRESS")
    key = ('swap_route', input_token, output_token, amount_lamports, from_address, slippage, anti_mev)
    if key in cache:
        return cache[key]
    url = f"{GMGN_API_HOST}/defi/router/v1/sol/tx/get_swap_route?token_in_address={input_token}&token_out_address={output_token}&in_amount={amount_lamports}&from_address={from_address}&slippage={slippage}"
    if anti_mev:
        url += "&is_anti_mev=true&fee=0.002"
    try:
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()['data']
        route_plan = data['quote']['routePlan']
        bundle_ratio = len(route_plan) / (data.get('tx_count', 1) or 1)
        price_impact = float(data['quote']['priceImpact']) if data['quote']['priceImpact'] is not None else 0
        alpha = "Dump risk" if price_impact > 10 else "Stable liq – watch support"
        result = {
            "bundle_ratio": bundle_ratio,
            "price_impact": price_impact,
            "alpha": alpha,
            "raw_tx": data['raw_tx']['swapTransaction']
        }
        cache[key] = result
        return result
    except Exception as e:
        return {"error": str(e)}

def get_holders(token):
    """Gets holders list from GMGN API, with caching."""
    key = ('holders', token)
    if key in cache:
        return cache[key]
    url = f"{GMGN_API_HOST}/defi/quotation/v1/tokens/sol/{token}/holders"
    try:
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        result = response.json()
        cache[key] = result
        return result
    except Exception as e:
        return {"error": str(e)}
