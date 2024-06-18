from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserModel(BaseModel):
    email: str
    password: str
    cpf: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    token: Optional[str] = None

class UserGet(BaseModel):
    id: str
    name: str
    email: str
    role: str    
    created_at: Optional[datetime]
    deleted: Optional[bool] = None
    token: Optional[str] = None

class UserList(BaseModel):
    rooms: list[UserGet]