"""Local database configuration shared by the application and migrations."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")


def get_database_url() -> str:
    """Read configuration without placing credentials in error messages."""
    value = os.environ.get("DATABASE_URL")
    if value is None or not value.strip():
        raise RuntimeError("DATABASE_URL must be configured in the environment or local .env")
    return value
