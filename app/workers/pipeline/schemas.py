from typing import List, Optional
from pydantic import BaseModel, Field

class TimelineExtraction(BaseModel):
    stage_name: str = Field(description="The name of the timeline stage or milestone, e.g. 'Pendaftaran Gelombang 1'")
    due_date: str = Field(description="ISO 8601 format date of the deadline/due date, e.g. '2026-05-30'")


class CategoryExtraction(BaseModel):
    name: str = Field(description="The name of the competition sub-category or branch, e.g. 'Band Competition'")
    price: float = Field(description="Registration fee amount, 0.0 if free")
    contact_person: Optional[str] = Field(description="Contact person details specific to this category")


class CompetitionExtraction(BaseModel):
    title: str = Field(description="Official full title of the competition event")
    organizer: str = Field(description="Name of the hosting institution or organizing committee")
    description: str = Field(description="Concise description/theme summary of the event")
    registration_link: Optional[str] = Field(description="Registration link URL if present, e.g. forms.gle/abc")
    guidebook_link: Optional[str] = Field(description="Juknis/guidebook shortlink URL if present")
    general_contacts: Optional[str] = Field(description="General contact info block, e.g. WhatsApp, Line, or Email")
    timelines: List[TimelineExtraction] = Field(description="Timeline schedules of the event")
    categories: List[CategoryExtraction] = Field(description="Branches or pricing categories of the competition")
