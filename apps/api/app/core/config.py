from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CalcSteam API"
    app_env: str = "development"
    app_secret: str = "change_me"
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "postgresql+psycopg://user:pass@localhost:5432/steam_topup"
    encryption_key: str = "Z0FBQUFBQm5fRHVNT0lSNFhYbE9aaGdLRjA2OGV0R0hqX2d3WXotS2QxSUpwX2o0NURfM2pKTDR2dXpWWHJtN2t3dExxQ2V4U3RlRkFhN3VvYlR4M2Z6Q1RfdmJfS1E9PQ=="
    reservation_ttl_minutes: int = 15

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
