from pydantic import BaseModel,Field
from uuid import UUID
from typing import Optional

class UserBase (BaseModel):
    name:str
    email:str
    

class UserCreate (UserBase):
    password: str = Field(min_length=6, max_length=72)
    

class UserUpdate (BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    
class UserResponse(UserBase):
    id: UUID