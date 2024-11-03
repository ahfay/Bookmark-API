from sqlmodel import SQLModel, create_engine, Session
from ..setting import db_settings
from .user import UserSchema
from .bookmark import BookmarkSchema

engine = create_engine(db_settings.db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
