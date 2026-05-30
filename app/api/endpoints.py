from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.schemas.post import InstagramPostResponse
from app.schemas.response import APIResponse
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
    )
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
        return APIResponse(
            status="success",
            message=f"Successfully scraped {len(posts)} posts from @{username}",
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

