# ===== Imports =====
from pwdlib import PasswordHash


# ===== Paroles hešošanas algoritms (Argon2) =====
password_hash = PasswordHash.recommended()

# ===== Paroles hešošanās funkcija =====
def get_password_hash(password):
    return password_hash.hash(password)


# ===== Paroļu salīdzināšanas funkcija =====
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
