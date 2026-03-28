from fastapi import HTTPException
from app.core.security.hashed import hash_password, verify_password
from app.core.security.token import create_token
from app.modules.user.user_repository import UserRepository


class AuthService:

    def __init__(self, repo: UserRepository):
        self.repo = repo


    def register(self, data):

        user_exists = self.repo.get_by_email(data.email)

        if user_exists:
            raise HTTPException(400, "Email ja cadastrado")

        data.password = hash_password(data.password)

        return self.repo.create(data)


    def login(self, data):

        user = self.repo.get_by_email(data.email)

        if not user:
            raise HTTPException(400, "Credenciais invalidas")

        if not verify_password(data.password, user.password):
            raise HTTPException(400, "Credenciais invalidas")


        token = create_token({
            "user_id": str(user.id),
            "role": user.role
        })


        return {
    "access_token": token,
    "token_type": "bearer",
    "user": user,
    "role": user.role
}