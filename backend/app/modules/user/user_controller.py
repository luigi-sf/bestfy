from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.modules.user.user_repository import UserRepository
from app.modules.user.user_service import UserService
from app.modules.user.user_schema import UserCreate, UserUpdate, UserResponse
from app.core.security.dependencies import get_current_user, get_optional_user, require_role
from app.models.user import User
from app.models.blacklist import TokenBlacklist
from app.core.security.dependencies import oauth2_scheme

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


#lista usuários - ADMIN
@router.get("/", response_model=list[UserResponse])  
def list_users(service: UserService = Depends(get_user_service),
               ):
    return service.list()


#Criar usuário 
@router.post("/", response_model=UserResponse, status_code=201)
def create(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create(user)


# Rota logado
@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(user: UserUpdate, service: UserService = Depends(get_user_service),
              current_user: User = Depends(get_current_user)):
    return service.update(current_user.id, user)


# get_by_id - ADMIN
@router.get("/by-id/{user_id}", response_model=UserResponse)
def get_by_id(user_id: UUID, service: UserService = Depends(get_user_service),
              current_user: User = Depends(require_role(["admin"]))):
    return service.get_by_id(user_id)


@router.put("/by-id/{user_id}", response_model=UserResponse)
def update(user_id: UUID, user: UserUpdate, service: UserService = Depends(get_user_service),
           current_user: User = Depends(require_role(["admin"]))):
    return service.update(user_id, user, current_user)


# Logout 
@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
):
    service.logout(token)
    return {"message": "Logged out successfully"}


#  Deletar próprio usuário
@router.delete("/me", response_model=UserResponse)
def delete_me(service: UserService = Depends(get_user_service),
              current_user: User = Depends(get_current_user)):
    return service.delete(current_user.id)


# Deletar outro usuário - ADMIN
@router.delete("/by-id/{user_id}", response_model=UserResponse)
def delete(user_id: UUID, service: UserService = Depends(get_user_service),
           current_user: User = Depends(require_role(["admin"]))):
    return service.delete(user_id)