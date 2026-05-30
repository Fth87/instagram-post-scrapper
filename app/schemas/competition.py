from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Timeline schemas
class CompetitionTimelineResponse(BaseModel):
    id: int
    competition_id: int
    stage_name: str
    due_date: datetime

    class Config:
        from_attributes = True


# Category schemas
class CompetitionCategoryResponse(BaseModel):
    id: int
    competition_id: int
    name: str
    price: float
    contact_person: Optional[str] = None

    class Config:
        from_attributes = True


# Competition schemas
class CompetitionResponse(BaseModel):
    id: int
    title: str
    organizer: str
    description: str
    image_url: str
    registration_link: Optional[str] = None
    guidebook_link: Optional[str] = None
    general_contacts: Optional[str] = None
    instagram_shortcode: Optional[str] = None
    created_at: datetime
    timelines: List[CompetitionTimelineResponse] = []
    categories: List[CompetitionCategoryResponse] = []

    class Config:
        from_attributes = True


# Raw staging post schema
class RawStagingPostResponse(BaseModel):
    id: int
    instagram_shortcode: str
    raw_caption: str
    image_url: str
    scraped_at: datetime
    is_processed: bool
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Background pipeline status schema
class PipelineStatusResponse(BaseModel):
    is_running: bool
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    total_to_process: int
    processed_count: int
    failed_count: int
    currently_processing: Optional[str] = None
    errors: List[str] = []

    class Config:
        from_attributes = True
