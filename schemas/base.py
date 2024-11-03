from pydantic import BaseModel, validator, Field, HttpUrl
from fastapi import HTTPException
from datetime import datetime
from urllib.parse import urlparse

class ErrorResponse(BaseModel):
    detail: str

class MessageBase(BaseModel):
    status: bool = Field(default=True)
    message: str
    
class TokenBase(BaseModel):
    access_token: str | None
    
class UserBase(BaseModel):
    username: str 
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise HTTPException(status_code=400, detail="The username character format used is alphanumeric")
        return v
    
class BookmarkDetailsBase(BaseModel):
    id: int
    body: str
    url: HttpUrl
    short_url: str
    created_at: datetime
    
class BookmarkRequestBase(BaseModel):
    body: str | None
    url: str
    @validator("url")
    def validate_url(cls, v):
        parsed_url = urlparse(v)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise HTTPException(status_code=400, detail="Invalid URL format. Please provide a valid URL.")
        return v
    
class ShortUrlBase(BaseModel):
    short_url: str | None = Field(default=None)
    @validator("short_url")
    def validate_short_url(cls, v):
        if not v.isalnum() and v is not None :
            raise HTTPException(status_code=400, detail="The short URL character format used is alphanumeric")
        return v