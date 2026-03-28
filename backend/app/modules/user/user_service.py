from fastapi import HTTPException
from app.modules.user.user_repository import UserRepository
from app.modules.user.user_schema import UserCreate, UserUpdate
from uuid import UUID


class UserService:
    
    def __init__(self, repo:UserRepository):
        self.repo = repo
        
    
    def create(self, user: UserCreate):
        
        user_exist = self.repo.get_by_email(user.email)
        
        if user_exist:
            raise HTTPException(
                status_code=400,
                detail='Email ja cadastrado'
            )
            
        return self.repo.create(user)
    
    
    def list (self):
        return self.repo.list()
    
    
    def get_by_id(self, user_id:UUID):
        
        user = self.repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail='usuario nao encontrado'
            )
            
        return user
    
    
    def update(self, user_id, data, current_user=None):

        db_user = self.repo.update(user_id, data)

        if not db_user:
            raise HTTPException(404, "User not found")

        return db_user
    
    
    def delete (self,user_id:UUID):
        
        user = self.repo.delete(user_id)
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail='usuario nao encontrado'
            )