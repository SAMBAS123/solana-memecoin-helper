import time
import asyncio
from dotenv import load_dotenv
import os
from scipy.signal import find_peaks
from liquidity import get_liquidity
from notify import send_alert

load_dotenv()

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 300))  # 5 min default
LIQ_DROP_THRESHOLD = float(os.getenv("LIQ_DROP_THRESHOLD", -10))  # % change for alert

async def liq_ta(token, historical_data=None):
    """Enhanced liquidity TA with scipy for support/resistance."""
    liq = get_liquidity(token)
    if 'error' in liq:
        return liq
    change = liq["liquidity_change_5m"]
    alpha = "Dump risk" if change < LIQ_DROP_THRESHOLD else "Stable liq"
    if historical_data:
        # Enhance with scipy: detect peaks (resistance) and valleys (support)
        changes = [d["liquidity_change_5m"] for d in historical_data]
        peaks, _ = find_peaks(changes)  # Resistance levels
        valleys, _ = find_peaks([-c for c in changes])  # Support levels
        alpha += f" (Peaks: {len(peaks)}, Valleys: {len(valleys)})"
    return {"liquidity_usd": liq["liquidity_usd"], "change_5m": change, "alpha": alpha}

async def poll_liquidity(token, duration=3600):
    """Basic async polling for liquidity monitoring."""
    start_time = time.time()
    historical = []
    while time.time() - start_time < duration:
        liq = await liq_ta(token, historical)
        historical.append(liq)
        if 'error' not in liq and liq["change_5m"] < LIQ_DROP_THRESHOLD:
            send_alert(f"Liquidity drop alert for {token}: {liq['change_5m']}% - {liq['alpha']}")
        await asyncio.sleep(POLL_INTERVAL)
    return historical
