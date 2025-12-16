
import os
from pydantic import BaseModel

def detect_database_url() -> str:
    # If DATABASE_URL present (Railway usually provides this), use it.
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # Normalize if needed
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return db_url
    # Else compose from PG* variables used by Railway
    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT")
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    database = os.getenv("PGDATABASE")
    if host and port and user and password and database:
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    # Fallback (dev only): sqlite
    return "sqlite:///./webaudit.sqlite3"

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Web Audit Platform")
    api_v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
    secret_key: str = os.getenv("SECRET_KEY", "dev_secret_key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    database_url: str = detect_database_url()
    from_email: str = os.getenv("FROM_EMAIL", "no-reply@webaudit.local")
    base_url: str = os.getenv("BASE_URL", "http://localhost:8000")

settings = Settings()
