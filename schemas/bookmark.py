from pydantic import BaseModel, Field
from .base import MessageBase, BookmarkDetailsBase, BookmarkRequestBase, ShortUrlBase
from datetime import datetime


class AddBookmarkRequest(BookmarkRequestBase, ShortUrlBase):
    pass
    
class AddBookmarkResponse(MessageBase):
    data: BookmarkDetailsBase
    
class ReadAllBookmarksResponse(BookmarkDetailsBase):
    updated_at: datetime | None = Field(default=None)
    visits: int
    
class UpdateBookmarkRequest(ShortUrlBase):
    body: str | None
    
class UpdateBookmarkResponse(MessageBase):
    data: ReadAllBookmarksResponse

class DeleteBookmarkResponse(MessageBase):
    pass
    