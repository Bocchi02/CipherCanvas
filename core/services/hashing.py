import hashlib

def generate_sha256(text: str) -> str:
    """Generates a SHA-256 hash for the given text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def generate_file_sha256(file_path: str) -> str:
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()

def verify_integrity(message: str, stored_hash: str):
    generated_hash = generate_sha256(message)

    return {
        "generated_hash": generated_hash,
        "stored_hash": stored_hash,
        "is_match": generated_hash == stored_hash
    }

def verify_file_integrity(file_path: str, stored_hash: str):
    generated_hash = generate_file_sha256(file_path)

    return {
        "generated_hash": generated_hash,
        "stored_hash": stored_hash,
        "is_match": generated_hash == stored_hash
    }
