import hashlib

def generate_sha256(text: str) -> str:
    """Generates a SHA-256 hash for the given text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def verify_integrity(message: str, stored_hash: str):
    generated_hash = generate_sha256(message)

    return {
        "generated_hash": generated_hash,
        "stored_hash": stored_hash,
        "is_match": generated_hash == stored_hash
    }