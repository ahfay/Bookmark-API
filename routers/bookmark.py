from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlmodel import Session
from ..models.db import get_session
from ..schemas.bookmark import (AddBookmarkRequest, AddBookmarkResponse, ReadAllBookmarksResponse, UpdateBookmarkRequest,
                                UpdateBookmarkResponse, DeleteBookmarkResponse)
from ..crud.bookmark import (add_bookmark_handler, read_all_bookmarks_handler, update_one_bookmark_handler,
                             delete_one_bookmark_handler)
from fastapi_pagination import Page, Params


router = APIRouter(
    prefix="/bookmark",
    tags=['Bookmark']
)

@router.post("/add", 
             status_code=201,
             response_model=AddBookmarkResponse)
async def add_bookmark(bookmark: AddBookmarkRequest, auth: AuthJWT = Depends(), session: Session = Depends(get_session)):
    auth.jwt_required()
    result = add_bookmark_handler(session=session, bookmark=bookmark, user_id=auth.get_jwt_subject())
    return AddBookmarkResponse(message="Bookmark successfully added to the database", data=result)

@router.get("/all",
            response_model=Page[ReadAllBookmarksResponse])
async def read_all_bookmarks(session: Session = Depends(get_session), auth: AuthJWT = Depends(), params: Params = Depends()):
    auth.jwt_required()
    response = read_all_bookmarks_handler(session=session, user_id=auth.get_jwt_subject(), params=params)
    return response

@router.put("/{bookmark_id}",
            status_code=201,
            response_model=UpdateBookmarkResponse)
async def update_bookmark(bookmark_id: int, bookmark: UpdateBookmarkRequest,
                          session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    auth.jwt_required()
    result = update_one_bookmark_handler(session=session, bookmark_id=bookmark_id, bookmark_new=bookmark, user_id=auth.get_jwt_subject())
    return UpdateBookmarkResponse(message="Bookmark successfully updated", data=result)

@router.delete("/{bookmark_id}",
               status_code=200,
               response_model=DeleteBookmarkResponse)
async def delete_bookmark(bookmark_id: int,session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    auth.jwt_required()
    response = delete_one_bookmark_handler(session=session, bookmark_id=bookmark_id, user_id=auth.get_jwt_subject())
    return response