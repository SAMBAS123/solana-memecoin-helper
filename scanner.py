from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

from utils import get_swap_route
from holder_scanner import scan_holders
from notify import send_alert
from scipy.signal import find_peaks  # For liq TA peaks

load_dotenv()

def fast_memecoin_scan(token, mc_threshold=None):
    """Performs fast parallel scan of memecoin holders and liquidity/bundle info."""
    if mc_threshold is None:
        mc_threshold = int(os.getenv("MC_THRESHOLD", 10000))
    bundle_ratio_threshold = float(os.getenv("BUNDLE_RATIO_THRESHOLD", 1))
    mc_low_threshold = int(os.getenv("MC_LOW_THRESHOLD", 20000))

    with ThreadPoolExecutor() as executor:
        future_holders = executor.submit(scan_holders, token)
        future_bundle_liq = executor.submit(get_swap_route, output_token=token)

    holders = future_holders.result()
    bundle_liq = future_bundle_liq.result()

    if isinstance(bundle_liq, dict) and 'error' not in bundle_liq:
        bundle_ratio = bundle_liq.get("bundle_ratio", 0)
        if bundle_ratio > bundle_ratio_threshold or (mc_threshold < mc_low_threshold and bundle_ratio > bundle_ratio_threshold):
            send_alert(f"Risky bundle ratio for {token}")

    return {"holders": holders, "bundle_liq": bundle_liq, "alpha": "Buy signal" if bundle_liq.get("priceImpact") is not None and bundle_liq.get("priceImpact") < 5 else "Dump risk"}

def liq_ta(token):
    """Stub for liquidity technical analysis with peaks."""
    # TODO: Implement actual TA using API data and scipy
    return {"peaks": []}  # Placeholder

def quick_scan(token, mc_threshold=10000):
    """Fast scan integration (parallel with holders/liq)."""
    with ThreadPoolExecutor() as executor:
        future_gmgn = executor.submit(get_swap_route, token)
        future_holders = executor.submit(scan_holders, token)
        future_liq = executor.submit(liq_ta, token)
    gmgn = future_gmgn.result()
    if gmgn.get('bundle_ratio', 0) > 1 and mc_threshold < 20000:
        send_alert(f"Risky bundle >1:1 for {token} – Skip!")
    return {"gmgn": gmgn, "holders": future_holders.result(), "liq_alpha": future_liq.result()}
