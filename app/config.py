import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEFAULT_TZ: str = os.getenv("DEFAULT_TZ", "Africa/Lagos")

settings = Settings()
