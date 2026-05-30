from fastapi import APIRouter, Query, Request, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from sqlmodel import Session, select
from app.schemas.post import InstagramPostResponse
from app.schemas.response import APIResponse
from app.database import get_db
from app.models.raw_post import RawInstagramPost
from app.services.instagram import (
    InstagramClientManager,
    InstagramScraperService,
    InstagramRateLimitException
)

# Router configuration
router = APIRouter(prefix="/instagram", tags=["Instagram Scraper"])

# Instantiate the service layer with dependency injection
instagram_client = InstagramClientManager()
instagram_service = InstagramScraperService(client_manager=instagram_client)

@router.get("/scrape", response_model=APIResponse[list[InstagramPostResponse]])
async def scrape_latest_posts(
    request: Request,
    username: str = Query(
        ..., 
        description="The public Instagram username to scrape", 
        example="instagram"
    ),
    limit: int = Query(
        5, 
        ge=1, 
        le=20, 
        description="Number of latest posts to retrieve (max 20 to prevent rate-limiting)"
    ),
    db: Session = Depends(get_db)
):
    """
    Scrape the latest posts from a public Instagram account.
    
    This endpoint retrieves:
    - **Post Caption**: Raw caption text.
    - **Post Photo**: Downloads the image locally and returns an absolute, persistent host URL.
    - **Metadata**: Published timestamp (UTC), likes count, and comments count.
    
    *Under the hood, blocking sync operations are offloaded to a background threadpool to maintain high API responsiveness.*
    """
    base_url = str(request.base_url)

    try:
        # Run blocking Instaloader sync logic in Starlette's threadpool
        posts = await run_in_threadpool(
            instagram_service.scrape_latest_posts_sync,
            username=username.strip().lower(),
            limit=limit,
            base_url=base_url
        )
        
        # Save scraped posts to the raw_instagram_posts staging database
        new_saved_count = 0
        duplicate_count = 0
        
        for post in posts:
            # Check if post already exists in staging database to prevent duplicate entries
            statement = select(RawInstagramPost).where(RawInstagramPost.instagram_shortcode == post["shortcode"])
            existing_post = db.exec(statement).first()
            
            if not existing_post:
                new_raw = RawInstagramPost(
                    instagram_shortcode=post["shortcode"],
                    raw_caption=post["caption"] or "",
                    image_url=post["image_url"],
                    is_processed=False
                )
                db.add(new_raw)
                new_saved_count += 1
            else:
                duplicate_count += 1
                
        if new_saved_count > 0:
            db.commit()
            
        message = (
            f"Successfully scraped {len(posts)} posts from @{username}. "
            f"Database status: {new_saved_count} new posts added to staging, "
            f"{duplicate_count} already existed."
        )
        
        return APIResponse(
            status="success",
            message=message,
            data=posts
        )
        
    except InstagramRateLimitException as rle:
        # Catch custom Instagram rate limiting exception and respond with HTTP 429
        raise HTTPException(status_code=429, detail=str(rle))
    except ValueError as ve:
        # Profile not found
        raise HTTPException(status_code=404, detail=str(ve))
    except RuntimeError as re:
        # Connection or Instagram blocking issue
        raise HTTPException(status_code=503, detail=str(re))

