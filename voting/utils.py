import hashlib
import hmac
import os


def verification_hash(value: str) -> str:
    salt = os.environ.get("VOTE_HASH_SALT", "development-only-change-me").encode()
    normalized = value.strip().upper().encode()
    return hmac.new(salt, normalized, hashlib.sha256).hexdigest()
