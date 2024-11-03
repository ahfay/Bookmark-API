from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr

class UserSchema(SQLModel, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime | None = Field(sa_column_kwargs={'onupdate':datetime.now()})