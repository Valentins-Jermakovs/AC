# Imports
from pwdlib import PasswordHash


"""
===== Password Service =====

This module provides password hashing and verification functionality using the Argon2 algorithm.

Functions:

1. get_password_hash(password: str) -> str
   - Purpose: Hashes a plain text password.
   - Input: Plain text password.
   - Output: Hashed password string.
   - Notes: Uses Argon2 algorithm for secure hashing.

2. verify_password(plain_password: str, hashed_password: str) -> bool
   - Purpose: Verifies if a plain text password matches a hashed password.
   - Input: 
       - plain_password: The password provided by the user.
       - hashed_password: The stored hashed password from the database.
   - Output: True if the passwords match, False otherwise.
   - Notes: Uses Argon2 verification to ensure security.

   Remarks:
   - This service has built in salting and hashing to make password storage more secure.
"""


# Password hashing algorithm (Argon2)
password_hash = PasswordHash.recommended()

# Password hashing function
def get_password_hash(password):
    return password_hash.hash(password)

# Password verification
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
