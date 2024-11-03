from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from .crud.bookmark import redirect_to_url_handler
from .routers import user, bookmark
from fastapi_jwt_auth.exceptions import AuthJWTException
from .utils.auth import authjwt_exception_handler
from fastapi_pagination import add_pagination
from sqlmodel import Session
from .models.db import get_session

app = FastAPI()
app.include_router(user.router)
app.include_router(bookmark.router)
app.add_exception_handler(AuthJWTException, authjwt_exception_handler)
add_pagination(app)

@app.get("/{short_url}")
async def redirect_to_url(short_url : str, session: Session = Depends(get_session)):
    response = redirect_to_url_handler(session=session, short_url=short_url)
    return RedirectResponse(response)
