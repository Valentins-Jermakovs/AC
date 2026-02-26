# =========================
# Password Service
# =========================

from pwdlib import PasswordHash

"""
This module handles password hashing and verification using the Argon2 algorithm.

It is used by authentication and user management services to securely store and validate passwords.
"""


# Initialize recommended Argon2 password hasher
password_hash = PasswordHash.recommended()


# =========================
# Hash a password
# =========================
async def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using Argon2.

    :param password: Plain text password to hash
    :return: Hashed password string
    :notes: Uses secure salting and Argon2 hashing
    """
    return password_hash.hash(password)

# =========================
# Verify a password
# =========================
async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a stored hash.

    :param plain_password: Password provided by user
    :param hashed_password: Hashed password stored in database
    :return: True if passwords match, False otherwise
    :notes: Uses Argon2 verification for security
    """
    return password_hash.verify(plain_password, hashed_password)
