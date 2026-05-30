import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if it exists
load_dotenv(dotenv_path=BASE_DIR / ".env")


# Directory where scraped media (images) will be saved
MEDIA_DIR = BASE_DIR / "media"

# Instagrapi configuration settings
INSTAGRAM_SESSIONID = os.getenv("INSTAGRAM_SESSIONID", "")
RESIDENTIAL_PROXY_URL = os.getenv("RESIDENTIAL_PROXY_URL", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Ensure the media directory exists
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

