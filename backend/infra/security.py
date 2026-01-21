import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Gera hash seguro da senha
def get_password_hash(password: str) -> str:
    # Salt aleatório
    salt = os.urandom(16)
    # KDF (Key Derivation Function) com PBKDF2 + SHA256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = kdf.derive(password.encode("utf-8"))
    # Guardamos salt + hash juntos (base64) para poder verificar depois
    return base64.b64encode(salt + key).decode("utf-8")

# Verifica senha informada contra hash armazenado
def verify_password(plain_password: str, stored_hash: str) -> bool:
    data = base64.b64decode(stored_hash.encode("utf-8"))
    salt, key = data[:16], data[16:]
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    try:
        kdf.verify(plain_password.encode("utf-8"), key)
        return True
    except Exception:
        return False
