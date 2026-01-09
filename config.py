"""Configuration module for api.data.gov API settings."""

import os
from pathlib import Path


def load_dotenv():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


load_dotenv()


class Config:
    """Configuration class for API settings."""

    API_KEY = os.getenv("DATA_GOV_API_KEY")
    BASE_URL = "https://api.data.gov"

    # Congress.gov API endpoints
    CONGRESS_API_BASE = "https://api.congress.gov/v3"

    # Request settings
    TIMEOUT = 30
    MAX_RETRIES = 3

    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.API_KEY:
            raise ValueError(
                "DATA_GOV_API_KEY environment variable is not set. "
                "Get your API key from https://api.data.gov/signup/"
            )
        return True
