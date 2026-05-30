from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class InstagramPostResponse(BaseModel):
    shortcode: str = Field(..., description="Unique identifier for the Instagram post")
    caption: Optional[str] = Field(None, description="The raw caption text of the post")
    image_url: str = Field(..., description="The absolute local URL to access the downloaded post image")
    timestamp: datetime = Field(..., description="The date and time the post was published (UTC)")
    likes: int = Field(..., description="Total likes on the post at the time of scraping")
    comments_count: int = Field(..., description="Total comments count on the post")

    class Config:
        json_schema_extra = {
            "example": {
                "shortcode": "C5edaaa0",
                "caption": "Exploring the beautiful city of Jakarta! #travel",
                "image_url": "http://localhost:8000/media/instagram/C5edaaa0.jpg",
                "timestamp": "2026-05-30T10:00:00Z",
                "likes": 1250,
                "comments_count": 42
            }
        }
