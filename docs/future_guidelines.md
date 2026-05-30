# Future Integrations Blueprint (Database, CRUD, and LLM)

This document serves as an architectural blueprint to guide you in adding future capabilities—such as Database/SQLModel persistence, CRUD APIs, and Multimodal LLM (Gemini AI) pipelines—while keeping the codebase clean, modular, and maintainable.

---

## 1. Database and CRUD Integration (SQLModel and Alembic)

To persist crawled metadata so that it is not lost after a server reload, we recommend using **SQLModel** (which combines SQLAlchemy and Pydantic).

### Steps
1. Create a new directory **`app/models/`** to store your database schema.
2. Declare your database connection interface in **`app/database.py`**.

### Database Schema Design (`app/models/post.py`)
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class InstagramPost(SQLModel, table=True):
    """
    SQLModel representation that serves as both a Database Schema
    and a Pydantic Model.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    shortcode: str = Field(index=True, unique=True)
    caption: Optional[str] = Field(default=None)
    image_url: str
    timestamp: datetime
    likes: int
    comments_count: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Injecting Database Sessions into Routes
Use FastAPI's Dependency Injection (`Depends`) to safely inject the active database session into your API endpoints:

```python
# app/database.py
from sqlmodel import create_engine, Session

sqlite_url = "sqlite:///./instagram_scraper.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_db():
    with Session(engine) as session:
        yield session
```

In `app/api/endpoints.py`, inject the session utility:
```python
@router.get("/scrape")
async def scrape_posts(db: Session = Depends(get_db)):
    # ... perform scraping and write to db ...
```

---

## 2. LLM Pipeline Integration (Gemini AI API)

Once you scrape and save post covers and captions locally, you can feed them to the **Gemini API** for multimodal extraction tasks (such as category tag generation, sentiment analysis, or spam filtering).

### Steps
1. Create a new package under services: **`app/services/llm/`**.
2. Create **`app/services/llm/gemini.py`** and **`app/services/llm/__init__.py`**.

### Gemini Service Blueprint (`app/services/llm/gemini.py`)
```python
import google.generativeai as genai
from PIL import Image
from pathlib import Path
from app.config import GEMINI_API_KEY

class GeminiPipelineService:
    """
    Manages multimodal AI pipeline workflows using Gemini Flash.
    """
    def __init__(self):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def analyze_instagram_post(self, image_path: Path, caption: str) -> dict:
        """
        Sends the local cover image and caption text to Gemini Flash
        to obtain structured analytical insights.
        """
        if not self.model:
            raise ValueError("GEMINI_API_KEY is not configured in your .env file!")

        # Safely open the downloaded cover image
        if not image_path.exists():
            raise FileNotFoundError(f"Cover image file not found at: {image_path}")
        
        image = Image.open(image_path)

        # Structure prompt for clean JSON output
        prompt = (
            f"Analyze the following Instagram post:\n"
            f"Caption Text: '{caption}'\n\n"
            f"Provide a clean JSON output containing exactly the following keys: "
            f"'sentiment' (positive/negative/neutral), 'content_category', "
            f"'brief_summary', and 'recommended_hashtags'."
        )

        # Execute multimodal API request
        response = self.model.generate_content([prompt, image])
        
        return {
            "raw_analysis": response.text,
            "status": "success"
        }
```

---

## 3. Core Architectural Rules

1. **Strict Decoupling:** Do not write database SQL operations or make HTTP requests to the Gemini API directly inside your `app/api/endpoints.py` router file. Always isolate these logic blocks inside dedicated service classes within `app/services/`.
2. **Database Migrations:** When updating database models in production, always utilize **Alembic** to manage database schema upgrades instead of invoking `SQLModel.metadata.create_all(engine)` directly.
3. **Safe Asynchronous I/O:** Since model inference and database writes are blocking I/O tasks, execute their service methods via `run_in_threadpool` inside FastAPI's async route handlers to maintain high API responsiveness.
