from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, TEXT

class RawInstagramPost(SQLModel, table=True):
    """
    Represents the staging database table storing raw, un-cleansed Instagram post payloads
    crawled by the scraping service layer before LLM processing.
    """
    __tablename__ = "raw_instagram_posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    instagram_shortcode: str = Field(unique=True, index=True, nullable=False)
    raw_caption: str = Field(sa_column=Column(TEXT, nullable=False))
    image_url: str = Field(nullable=False)
    scraped_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_processed: bool = Field(default=False, index=True, nullable=False)
    processed_at: Optional[datetime] = Field(default=None, nullable=True)
