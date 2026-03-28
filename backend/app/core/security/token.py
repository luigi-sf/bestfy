from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose import JWTError


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',60))

def create_token(data: dict) -> str:
    payload = data.copy() # faz copia pra n alterar o origional
    payload["exp"] = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES) # expiracao do token 
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # token criado payload - encode - assinatura - JWT


def decode_token(token: str) -> dict | None: #decodentificacao de token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # verifica c ta td certo
        return payload
    except JWTError:
        return None