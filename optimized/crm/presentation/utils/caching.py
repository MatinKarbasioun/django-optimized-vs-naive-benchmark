import hashlib
import json


def generate_cache_key(prefix: str, params: dict) -> str:
    sorted_params = sorted(params.items())
    params_str = json.dumps(sorted_params)
    params_hash = hashlib.md5(params_str.encode('utf-8')).hexdigest()
    return f"{prefix}:{params_hash}"