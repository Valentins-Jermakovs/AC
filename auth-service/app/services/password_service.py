from pwdlib import PasswordHash

# === paroles hešošabas algoritms (Argon2) ===
password_hash = PasswordHash.recommended()
# password_hash satur metodes hash() un verify()
# === === === === === === === === === === ===

# === paroles hešošanās funkcija ===
# funkcija saņem tekstu
# atgriež hešotu paroli
def get_password_hash(password):
    return password_hash.hash(password)
# === === === === === === === === ===

# === paroles salīdzināšanas funkcija ===
# funkcija sagaida tekstu un hešotu paroli
# veic salīdzināšanu
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
# === === === === === === === === === === === ===


# === lietotāju verifikācijas funkcija ===
# funkcija atgriež lietotāju objektu
# kombinē iepriekš veidotas funkcijas
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user