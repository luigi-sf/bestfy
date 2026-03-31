from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import uuid

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60))


def create_token(data: dict) -> str:
    payload = data.copy()

    if "sub" not in payload or not payload["sub"]:
        raise ValueError("Token precisa de 'sub'")

    payload.update({
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "jti": str(uuid.uuid4())
    })

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None