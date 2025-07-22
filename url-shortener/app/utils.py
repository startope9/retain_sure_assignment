# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import string
import random
from urllib.parse import urlparse

def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url: str) -> bool:
    try:
        parts = urlparse(url)
        return parts.scheme in ('http', 'https') and bool(parts.netloc)
    except Exception:
        return False
