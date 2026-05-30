from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as instagram_router
from app.config import MEDIA_DIR
from app.exceptions import setup_exception_handlers
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database tables on startup
    init_db()
    yield

# Initialize FastAPI App
app = FastAPI(
    title="Instagram Scraper API",
    description="Clean, Simple, and Fast API to scrape public Instagram accounts, serve media locally, and prepare data for LLM pipelines.",
    version="1.0.0",
    lifespan=lifespan
)

# Mount the media directory to serve downloaded images locally via HTTP
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

# Setup global exception handlers
setup_exception_handlers(app)

# Register routes
app.include_router(instagram_router)

@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint showing API service status and quick instructions.
    """
    return {
        "service": "Instagram Scraper API",
        "status": "online",
        "message": "Welcome! Visit the interactive API documentation to test endpoints.",
        "docs_url": "/docs"
    }
