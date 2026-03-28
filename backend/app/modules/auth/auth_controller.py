from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.auth.auth_schema import UserRegister, UserLogin, TokenResponse
from app.modules.auth.auth_service import AuthService
from app.modules.user.user_repository import UserRepository
from app.core.database import get_db
from app.modules.user.user_schema import UserResponse
from app.models.blacklist import TokenBlacklist
from app.core.security.dependencies import oauth2_scheme
from app.core.security.dependencies import get_current_user

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return AuthService(repo)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserRegister,
    service: AuthService = Depends(get_auth_service)
):
    return service.register(user)


@router.post("/login", response_model=TokenResponse)
def login(
    user: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    return service.login(user)

@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    return current_user

@router.post('/logout')
def logout(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    
    black_listed = TokenBlacklist(token = token)
    
    db.add(black_listed)
    db.commit()
    
    return{'message': 'logged out'}