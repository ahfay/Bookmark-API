from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import HttpUrl

    
class BookmarkSchema(SQLModel, table=True):
    __tablename__ = 'bookmarks'
    id: int | None = Field(primary_key=True, default=None)
    body: str | None = Field(default=None)
    url: HttpUrl
    short_url: str
    visits: int = Field(default=0)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime | None = Field(sa_column_kwargs={'onupdate':datetime.now()})
    user_id: int | None = Field(default=None, foreign_key='users.id')    