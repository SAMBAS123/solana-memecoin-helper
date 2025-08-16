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
    with ThreadPoolExecutor() as executor:
        f_gmgn = executor.submit(get_gmgn_route, token)
        f_holders = executor.submit(scan_holders, token)
        f_liq = executor.submit(liq_ta, token)
    gmgn = f_gmgn.result()
    holders = f_holders.result()
    liq = f_liq.result()
    liq_history = [1000, 950, 900]  # Mock; replace with real from liq_ta history
    holder_pcts = [h.get('percentage', 0) for h in holders.get('data', [])] if isinstance(holders, dict) else []
    with ThreadPoolExecutor() as executor:
        f_rug = executor.submit(predict_rug, liq_history, holder_pcts)
    rug = f_rug.result()
    # Aggregate risk_score (0-100): e.g., impact*5 + max(holder_pct) + abs(liq_change)*2 + (100 if rug == "High rug risk" else 0) / 4
    impact = gmgn.get('impact', 0) if isinstance(gmgn, dict) else 0
    liq_change = liq.get('change_5m', 0) if isinstance(liq, dict) else 0
    max_pct = max(holder_pcts) if holder_pcts else 0
    rug_score = 100 if rug == "High rug risk" else 0
    risk_score = min(100, (impact * 5 + max_pct + abs(liq_change) * 2 + rug_score) / 4)
    if gmgn.get('bundle_ratio', 0) > 1 and mc_threshold < 20000:
        send_alert(f"Risky bundle >1:1 for {token}")
    return {"gmgn": gmgn, "holders": holders, "liq": liq, "rug": rug, "risk_score": risk_score}
