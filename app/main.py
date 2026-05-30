from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as instagram_router
from app.config import MEDIA_DIR

# Initialize FastAPI App
app = FastAPI(
    title="Instagram Scraper API",
    description=" Fast API Clean, Simple to scrape public Instagram accounts",
    version="1.0.0"
)

# Mount the media directory to serve downloaded images locally via HTTP
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

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
