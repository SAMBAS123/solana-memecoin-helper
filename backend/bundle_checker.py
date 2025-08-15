import os
import requests

JITO_BLOCK_ENGINE = os.getenv("JITO_BLOCK_ENGINE_URL", "https://mainnet.block-engine.jito.wtf")


def check_bundle(bundle_id: str):
    url = f"{JITO_BLOCK_ENGINE}/api/v1/bundles/{bundle_id}"
    resp = requests.get(url, timeout=20)
    if resp.status_code != 200:
        return {"ok": False, "status": resp.status_code}
    data = resp.json()
    return {"ok": True, "data": data}
