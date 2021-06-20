from .config import MIN_PASSWORD_LEN, BRANCA_SECRET, BRANCA_TTL
from .schemas import Payload

from branca import Branca
import bcrypt
import msgpack

branca = Branca(BRANCA_SECRET)

def hash_password(password: bytes):
  return bcrypt.hashpw(password, bcrypt.gensalt())

def check_password(password: bytes):
  if len(password) < MIN_PASSWORD_LEN:
    return False

  if password.isalnum():
    return False

  if not any([c.isupper() for c in list(password)]):
    return False

  return True

def verify_password(password: bytes, hashed: bytes):
  return bcrypt.checkpw(password, hashed)

def check_token(token: str, username: str):
  try:
    payload = branca.decode(token, ttl=BRANCA_TTL)
    data = msgpack.unpackb(payload, raw=False)
    data = Payload(**data)

    if data.get(username) == username:
       return data

  except RuntimeError as e:
    return

def decode_token(token: str):
  try:
    payload = branca.decode(token, ttl=BRANCA_TTL)
    data = msgpack.unpackb(payload, raw=False)
    data = Payload(**data)
    return data
  except RuntimeError as e:
    return

def create_token(username: str):
  payload = msgpack.packb({'username': username})
  token = branca.encode(payload)

  return token
