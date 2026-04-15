import hashlib

def generate_hash256(text: str) -> str:
    """Generates a SHA-256 hash for the given text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()