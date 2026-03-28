from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security.token import decode_token
from app.models.blacklist import TokenBlacklist
from app.core.database import get_db
from app.models.user import User

# 🔓 permite rotas públicas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login', auto_error=False)


# 🔒 USADO EM ROTAS PROTEGIDAS
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    black_list = db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
    if black_list:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


# 🔓 USADO EM ROTAS PÚBLICAS
def get_optional_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        return None

    payload = decode_token(token)
    if payload is None:
        return None

    return db.query(User).filter(User.id == payload["user_id"]).first()


# 🔒 ROLE BASED ACCESS
def require_role(roles: list[str]):
    def role_checker(user: User = Depends(get_current_user)):  # chama apenas quando necessário
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user
    return role_checker