from sqlmodel import Session, select, or_
from ..models.bookmark import BookmarkSchema
from fastapi import HTTPException

def check_url_or_shorturl_in_db(session: Session, url: str | None, short_url: str):
    result = session.exec(
        select(BookmarkSchema).where(or_(BookmarkSchema.url == url, BookmarkSchema.short_url == short_url))
    ).first()
    if result is not None:
        if result.short_url == short_url:
            raise HTTPException(status_code=409, detail="This short URL already uses")
        else:
            raise HTTPException(status_code=409, detail="This URL already in database")
    else:
        return result
    
def check_bookmark_exist_in_db(session: Session, bookmark_id: int, user_id: int) -> BookmarkSchema:
    result = session.exec(
        select(BookmarkSchema).where(BookmarkSchema.id == bookmark_id, BookmarkSchema.user_id == user_id)
    ).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return result