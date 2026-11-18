"""Password hashing.

PLANTED FLAW (OWASP A04:2025 Cryptographic Failures): passwords are hashed with
unsalted MD5. MD5 is fast, which is exactly what an attacker cracking a stolen
password table wants, and with no salt, identical passwords produce identical
hashes. The hardened version uses a slow, salted algorithm instead.
"""

import hashlib


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()
