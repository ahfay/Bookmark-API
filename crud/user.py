from sqlmodel import Session, select
from ..models.user import UserSchema
from ..schemas.user import UserLoginRequest, UserRegisterRequest, UserProfileResponse
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from ..utils.hash import generate_hash_passwords, password_hash_verification


def register_account_handler(session: Session, user: UserRegisterRequest, auth: AuthJWT) -> dict:
    try:
        add_user = UserSchema(username=user.username, password=generate_hash_passwords(user.password), email=user.email)
        session.add(add_user)
        session.commit()
        session.refresh(add_user)
        access_token = auth.create_access_token(subject=add_user.id, fresh=True)
        refresh_token = auth.create_refresh_token(subject=add_user.id)
        return {"access_token": access_token, "refresh_token":refresh_token}
    except:
        raise HTTPException(status_code=409, detail="username or email already in use")
           
def login_account_handler(session: Session, auth: AuthJWT, user: UserLoginRequest) -> dict:
    user_in_db = session.exec(
        select(UserSchema).where(UserSchema.username == user.username)).first()
    if user_in_db is not None and password_hash_verification(user.password, user_in_db.password):
        access_token = auth.create_access_token(subject=user_in_db.id, fresh=True)
        refresh_token = auth.create_refresh_token(subject=user_in_db.id)
        return {"access_token": access_token, "refresh_token":refresh_token}
    else:
        raise HTTPException(status_code=401, detail="Please provide valid authentication credentials.")

def read_profile_user(session: Session, auth: AuthJWT):
    current_user = auth.get_jwt_subject()
    user = session.exec(select(UserSchema).where(UserSchema.username == current_user)).first()
    return UserProfileResponse(message="User profile successfully obtained",
                               data={"username":current_user, "email":user.email, "created_at":user.created_at,
                                     "updated_at":user.updated_at})