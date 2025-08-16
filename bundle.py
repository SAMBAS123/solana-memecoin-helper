from utils import get_swap_route
from dotenv import load_dotenv
import os

load_dotenv()

def get_bundle_info(token):
    """Infers bundle info from swap route."""
    route = get_swap_route(output_token=token)
    if 'error' in route:
        return route
    return {
        "bundle_ratio": route["bundle_ratio"],
        "alpha": route["alpha"]
    }
