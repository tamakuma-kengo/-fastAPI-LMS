from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id:int
    username: str
    email: str
    created: datetime
    is_active: bool
    user_kind_id: int

class UserInDB(User):
    hashed_password: str
    
class UserCreate(BaseModel):
    username: str
    email: str
    created: datetime
    is_active: bool
    hashed_password: str
    user_kind_id: int
    
class UserKind(BaseModel):
    id: int
    kind_name: str
    create: bool

class UserKindCreate(BaseModel):
    kind_name: str
    create: bool