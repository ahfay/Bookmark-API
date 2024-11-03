from sqlmodel import Session, select, or_
from fastapi import HTTPException
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Params
from ..schemas.bookmark import AddBookmarkRequest, UpdateBookmarkRequest
from ..schemas.base import MessageBase
from ..models.bookmark import BookmarkSchema
from ..utils.hash import generate_short_url
from ..utils.valid import check_url_or_shorturl_in_db, check_bookmark_exist_in_db

def add_bookmark_handler(session: Session, bookmark: AddBookmarkRequest, user_id: int):
    bookmark_in_db = check_url_or_shorturl_in_db(session, bookmark.url, bookmark.short_url)
    if bookmark_in_db is None:
        short_url = bookmark.short_url
        if short_url is None:
            short_url = generate_short_url(bookmark.url)
        add_bookmark = BookmarkSchema(body=bookmark.body, url=bookmark.url, short_url=short_url, user_id=user_id)
        session.add(add_bookmark)
        session.commit()
        session.refresh(add_bookmark)
        return {"id":add_bookmark.id, "body":add_bookmark.body, "url":add_bookmark.url,
                "short_url":add_bookmark.short_url, "created_at":add_bookmark.created_at}
    
def read_all_bookmarks_handler(session: Session, params: Params, user_id: int):
    bookmark_in_db = select(BookmarkSchema).where(BookmarkSchema.user_id == user_id)
    if bookmark_in_db is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return paginate(session, bookmark_in_db, params)

def update_one_bookmark_handler(session: Session, bookmark_id: int, user_id: int, bookmark_new: UpdateBookmarkRequest):
    bookmark_old = check_bookmark_exist_in_db(session=session, bookmark_id=bookmark_id, user_id=user_id)
    bookmark_in_db = check_url_or_shorturl_in_db(session=session, short_url=bookmark_new.short_url, url=None)
    if bookmark_in_db is None:
        bookmark_old.body = bookmark_old.body if bookmark_new.body is None else bookmark_new.body
        bookmark_old.short_url = bookmark_old.short_url if bookmark_new.short_url is None else bookmark_new.short_url
        session.add(bookmark_old)
        session.commit()
        session.refresh(bookmark_old)
        return bookmark_old.dict()
    
def delete_one_bookmark_handler(session: Session, bookmark_id: int, user_id: int):
    bookmark_in_db = check_bookmark_exist_in_db(session=session, bookmark_id=bookmark_id, user_id=user_id)
    session.delete(bookmark_in_db)
    session.commit()
    return MessageBase(message=f"Bookmarks id-{bookmark_id} successfully deleted")
        
def redirect_to_url_handler(session: Session, short_url: str):
    bookmark_in_db = session.exec(
        select(BookmarkSchema).where(BookmarkSchema.short_url == short_url)
    ).first()
    if bookmark_in_db is None:
        raise HTTPException(status_code=404, detail="Content not found")
    bookmark_in_db.visits += 1
    session.add(bookmark_in_db)
    session.commit()
    return bookmark_in_db.url