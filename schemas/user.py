from pydantic import BaseModel, validator, EmailStr
from pydantic.errors import EmailError
from fastapi import HTTPException
from .base import UserBase, MessageBase, TokenBase
from datetime import datetime

class UserLoginRequest(UserBase):
    password: str
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise HTTPException(status_code=400, detail="minimum password 6 characters")
        return v

class UserLoginResponse(MessageBase):
    class AddRefreshToken(TokenBase):
        refresh_token: str | None
    data: AddRefreshToken
    
class UserRegisterRequest(UserLoginRequest):
    email: str
    @validator('email')
    def validate_email(cls, v):
        try:
            EmailStr.validate(v)
        except EmailError:
            raise HTTPException(status_code=400, detail="Invalid email format. Please provide a valid email address.")
        return v
    
class UserRegisterResponse(UserLoginResponse):
    pass

class UserProfileResponse(MessageBase):
    class ProfileDetail(BaseModel):
        username: str
        email: EmailStr
        created_at: datetime
        update_ate: datetime | None
    data: ProfileDetail