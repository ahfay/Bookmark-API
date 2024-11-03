from fastapi import Request, HTTPException
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from ..setting  import auth_settings

        
@AuthJWT.load_config
def get_config():
    return auth_settings

def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    if exc.message == "Signature has expired":
        raise HTTPException(status_code=401, detail=exc.message, )
    elif exc.message == "Missing Authorization Header":
        raise HTTPException(status_code=401, detail=exc.message)
    elif exc.message == "Not enough segments":
        raise HTTPException(status_code=422, detail=exc.message)
    elif exc.message == "The specified alg value is not allowed":
        raise HTTPException(status_code=422, detail=exc.message)
    elif exc.message == "Token has been revoked":
        raise HTTPException(status_code=401, detail=exc.message)
    elif exc.message == "Invalid claims":
        raise HTTPException(status_code=422, detail=exc.message)
    elif exc.message == "Missing CSRF token":
        raise HTTPException(status_code=401, detail=exc.message)
    elif exc.message == "CSRF double submit tokens do not match":
        raise HTTPException(status_code=401, detail=exc.message)
    else:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
    
denylist = set()
@AuthJWT.token_in_denylist_loader
def check_token_if_in_denylist(token):
    jti = token['jti']
    return jti in denylist