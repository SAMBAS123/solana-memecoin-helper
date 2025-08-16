from utils import get_holders

def scan_holders(token):
    """Scans holders via GMGN API, returns holder data."""
    return get_holders(token)
