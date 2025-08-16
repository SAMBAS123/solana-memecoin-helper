from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

from utils import get_swap_route
from holder_scanner import scan_holders
from notify import send_alert

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

    return {"holders": holders, "bundle_liq": bundle_liq, "alpha": bundle_liq.get("liq_alpha") if isinstance(bundle_liq, dict) else None}
