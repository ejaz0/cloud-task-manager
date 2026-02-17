from typing import Optional
from pydantic import BaseModel, EmailStr
from app.db.models import UserRole

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.USER
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
        # json_encoders = ...
