from pydantic import BaseSettings

        
class DBSetting(BaseSettings):
    db_url: str
    hash_algorithm: str
    class Config:
        env_file = ".env"
        
class AuthJWTSetting(BaseSettings):
    authjwt_secret_key: str
    authjwt_denylist_enabled: bool
    authjwt_denylist_token_checks: list
    class Config:
        env_file = ".env"
        
db_settings = DBSetting()
auth_settings = AuthJWTSetting()