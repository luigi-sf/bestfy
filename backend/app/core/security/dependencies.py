from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security.token import decode_token
from app.models.blacklist import TokenBlacklist
from app.core.database import get_db
from app.models.user import User
from app.modules.user.user_repository import UserRepository

# permite rotas públicas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login', auto_error=False)


# USADO EM ROTAS PROTEGIDAS
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    if not token:
        raise HTTPException(401, "Token não fornecido")

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(401, "Token inválido")

    jti = payload.get("jti")
    user_id = payload.get("sub")

    if not jti or not user_id:
        raise HTTPException(401, "Token inválido")

    # verifica blacklist corretamente
    blacklisted = db.query(TokenBlacklist).filter_by(jti=jti).first()

    if blacklisted:
        raise HTTPException(401, "Token inválido (logout realizado)")

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    return user


# USADO EM ROTAS PÚBLICAS
def get_optional_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if not token:
        return None

    payload = decode_token(token)
    if payload is None:
        return None

    jti = payload.get("jti")
    user_id = payload.get("sub")

    if not jti or not user_id:
        return None

    blacklisted = db.query(TokenBlacklist).filter_by(jti=jti).first()
    if blacklisted:
        return None

    return db.query(User).filter(User.id == user_id).first()

# ROLE ACCESS
def require_role(roles: list[str]):
    def role_checker(user: User = Depends(get_current_user)):  # chama apenas quando necessário
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user
    return role_checker