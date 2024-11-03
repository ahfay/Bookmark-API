from passlib.context import CryptContext
from ..setting import db_settings
from sqids import Sqids
import hashlib

context = CryptContext(schemes=[db_settings.hash_algorithm])

def generate_hash_passwords(password: str) -> str:
    return context.hash(password)

def password_hash_verification(password, hashed_passwords) -> bool:
    return context.verify(password, hashed_passwords)

def generate_short_url(url: str) -> str:
    url_numeric = int(hashlib.md5(url.encode()).hexdigest(), 16)
    sqids = Sqids(min_length=3)
    return sqids.encode([url_numeric % (9223372036854775807 + 1)])