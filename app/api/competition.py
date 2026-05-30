from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select, desc
from app.database import get_db
from app.schemas.response import APIResponse
from app.schemas.competition import CompetitionResponse, RawStagingPostResponse, PipelineStatusResponse
from app.models.raw_post import RawInstagramPost
from app.models.competition import Competition
from app.workers.pipeline import process_unprocessed_posts, pipeline_tracker

router = APIRouter(prefix="/competitions", tags=["Competition Management"])


@router.post("/process", response_model=APIResponse[None])
async def trigger_extraction_pipeline(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger the Multimodal LLM Extraction Pipeline.
    
    This endpoint executes the background worker asynchronously. It will:
    - Grab all unprocessed raw Instagram posts from the staging area database.
    - Resolve and open their local cover poster images.
    - Run multimodal queries to Gemini 1.5 Flash using strict JSON schemas.
    - Populate and structure main Competition, timelines, and category tables.
    
    *Returns immediately to the client with an HTTP 202 status, processing in the background without blocking.*
    """
    # Enqueue pipeline task using Starlette background tasks
    background_tasks.add_task(process_unprocessed_posts, db)
    
    return APIResponse(
        status="success",
        message="Multimodal extraction pipeline initiated successfully in the background.",
        data=None
    )


@router.get("/status", response_model=APIResponse[PipelineStatusResponse])
async def get_pipeline_status():
    """
    Check the status and progress of the background extraction pipeline.
    Returns detailed metrics on is_running, processed_count, failed_count, and any active errors.
    """
    return APIResponse(
        status="success",
        message="Successfully retrieved pipeline telemetry status.",
        data=pipeline_tracker
    )


@router.get("/raw", response_model=APIResponse[list[RawStagingPostResponse]])
async def list_raw_staging_posts(db: Session = Depends(get_db)):
    """
    Retrieve all raw, uncleansed posts currently stored in the staging database staging area.
    Useful for reviewing inbound scraper raw data before or after AI extraction.
    """
    statement = select(RawInstagramPost).order_by(desc(RawInstagramPost.scraped_at))
    raw_posts = db.exec(statement).all()
    
    return APIResponse(
        status="success",
        message=f"Successfully retrieved {len(raw_posts)} raw staging posts.",
        data=raw_posts
    )


@router.get("/extracted", response_model=APIResponse[list[CompetitionResponse]])
async def list_extracted_competitions(db: Session = Depends(get_db)):
    """
    Retrieve all successfully extracted competitions, complete with their timelines and categories.
    """
    statement = select(Competition).order_by(desc(Competition.created_at))
    competitions = db.exec(statement).all()
    
    return APIResponse(
        status="success",
        message=f"Successfully retrieved {len(competitions)} extracted structured competitions.",
        data=competitions
    )


@router.get("/", response_model=APIResponse[list[CompetitionResponse]])
async def list_all_competitions(db: Session = Depends(get_db)):
    """
    Alias endpoint to list all structured, extracted competitions.
    """
    statement = select(Competition).order_by(desc(Competition.created_at))
    competitions = db.exec(statement).all()
    
    return APIResponse(
        status="success",
        message=f"Successfully retrieved {len(competitions)} structured competitions.",
        data=competitions
    )
