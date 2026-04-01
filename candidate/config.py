from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    dashboard_api: str = os.getenv("DASHBOARD_API", "http://localhost:8000")
    scanner_api: str = os.getenv("SCANNER_API", "http://localhost:8001")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5433"))
    db_name: str = os.getenv("DB_NAME", "qa_test")
    db_user: str = os.getenv("DB_USER", "qa_user")
    db_password: str = os.getenv("DB_PASSWORD", "qa_password")

settings = Settings()
