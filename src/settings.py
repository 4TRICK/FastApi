from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int
    mongo_db_note_coll: str
    mongo_db_removed_note_coll: str
    mongo_db_auth_coll: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    testing: bool

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def get_mongo_detail(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"


@lru_cache
def get_settings():
    return Settings()
