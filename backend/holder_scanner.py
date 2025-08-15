import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple

load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")


def get_top_holders(token_address: str, limit: int = 10) -> List[Dict[str, Any]]:
    url = f"https://public-api.birdeye.so/defi/token_holders?address={token_address}&offset=0&limit={limit}"
    headers = {"X-API-KEY": BIRDEYE_API_KEY or "", "x-chain": "solana"}
    resp = requests.get(url, headers=headers, timeout=20)
    if resp.status_code != 200:
        return []
    return resp.json().get("data", {}).get("items", [])


def get_sol_balance_helius(wallet_address: str) -> Optional[float]:
    if not HELIUS_API_KEY:
        return None
    url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/balances?api-key={HELIUS_API_KEY}"
    resp = requests.get(url, timeout=20)
    if resp.status_code != 200:
        return None
    data = resp.json()
    lamports = data.get("nativeBalance", 0)
    return float(lamports) / 1e9


def is_rich_wallet(wallet_address: str, sol_threshold: float = 100.0) -> Tuple[bool, float]:
    sol_balance = get_sol_balance_helius(wallet_address)
    if sol_balance is not None and sol_balance >= sol_threshold:
        return True, sol_balance
    return False, sol_balance or 0.0


def scan_holders(token_address: str, holder_limit: int = 10, sol_threshold: float = 100.0) -> List[Dict[str, Any]]:
    holders = get_top_holders(token_address, limit=holder_limit)
    scanned = []
    for holder in holders:
        wallet = holder.get("address")
        ownership = holder.get("ownership")
        flag, bal = is_rich_wallet(wallet, sol_threshold=sol_threshold)
        scanned.append({"wallet": wallet, "sol_balance": bal, "ownership": ownership, "is_rich": flag})
    return scanned
