from pydantic import BaseModel
from app.modules.user.user_schema import UserResponse

class UserRegister (BaseModel):
    name:str
    email:str
    password:str
    


class UserLogin (BaseModel):
    email:str
    password:str
    
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    role: str