from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE_NUMBER: int

    MONGO_URI: str
    MONGO_DATABASE_NAME: str

    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int

    SECRET_KEY: str
    ALGORITHM: str

    CHANNEL_LIST_URL: str
    PODCAST_URL: str

    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
