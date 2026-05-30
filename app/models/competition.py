from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column, TEXT

class Competition(SQLModel, table=True):
    """
    Main parent database table storing primary, cleansed information about a competition
    after raw data has been parsed and structured by the LLM system.
    """
    __tablename__ = "competitions"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    organizer: str = Field(nullable=False)
    description: str = Field(sa_column=Column(TEXT, nullable=False))
    image_url: str = Field(nullable=False)
    registration_link: Optional[str] = Field(default=None, nullable=True)
    guidebook_link: Optional[str] = Field(default=None, nullable=True)
    general_contacts: Optional[str] = Field(sa_column=Column(TEXT, nullable=True))
    instagram_shortcode: Optional[str] = Field(default=None, unique=True, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships (Cascading on delete to clean up orphan child rows)
    timelines: list["CompetitionTimeline"] = Relationship(
        back_populates="competition",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    categories: list["CompetitionCategory"] = Relationship(
        back_populates="competition",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class CompetitionTimeline(SQLModel, table=True):
    """
    Child database table representing milestone roadmap deadlines and stages of a competition.
    """
    __tablename__ = "competition_timelines"

    id: Optional[int] = Field(default=None, primary_key=True)
    competition_id: int = Field(
        foreign_key="competitions.id",
        nullable=False,
        ondelete="CASCADE"
    )
    stage_name: str = Field(nullable=False)
    due_date: datetime = Field(nullable=False)

    # Back-populating relationship reference
    competition: Competition = Relationship(back_populates="timelines")


class CompetitionCategory(SQLModel, table=True):
    """
    Child database table representing branches, pricing categories, and local contact persons
    of a competition.
    """
    __tablename__ = "competition_categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    competition_id: int = Field(
        foreign_key="competitions.id",
        nullable=False,
        ondelete="CASCADE"
    )
    name: str = Field(nullable=False)
    price: float = Field(default=0.0, nullable=False)
    contact_person: Optional[str] = Field(default=None, nullable=True)

    # Back-populating relationship reference
    competition: Competition = Relationship(back_populates="categories")
