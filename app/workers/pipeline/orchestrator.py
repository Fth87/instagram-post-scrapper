from sqlmodel import Session, select
from app.config import GEMINI_API_KEY
from app.models.raw_post import RawInstagramPost
from app.workers.pipeline.tracker import pipeline_tracker
from app.workers.pipeline.extractor import GeminiExtractor
from app.workers.pipeline.repository import CompetitionRepository
from app.workers.pipeline.resolver import MediaResolver

def process_unprocessed_posts(db: Session) -> None:
    """
    Background worker orchestrator. Connects loader, AI extraction, and database persistence layers.
    """
    print("[*] Starting Multimodal LLM Extraction Pipeline...")
    
    if not GEMINI_API_KEY:
        print("[-] Pipeline Error: GEMINI_API_KEY is not configured in env parameters.")
        return

    # Ingestion Stage: Fetch unprocessed posts
    statement = select(RawInstagramPost).where(RawInstagramPost.is_processed == False)  # noqa: E712
    unprocessed_posts = db.exec(statement).all()

    if not unprocessed_posts:
        print("[*] Pipeline Status: No unprocessed raw posts found in staging database.")
        return

    # Initialization Stage
    extractor = GeminiExtractor(api_key=GEMINI_API_KEY)
    pipeline_tracker.start(len(unprocessed_posts))

    print(f"[*] Found {len(unprocessed_posts)} unprocessed posts to extract.")

    try:
        for raw_post in unprocessed_posts:
            shortcode = raw_post.instagram_shortcode
            print(f"[*] Processing post shortcode: {shortcode}...")
            pipeline_tracker.update_progress(shortcode)

            # 1. Resolve cover poster image file
            img = MediaResolver.load_local_image(raw_post.image_url)
            if img:
                print(f"[+] Loaded local poster image for multimodal analysis: {shortcode}.jpg")
            else:
                print(f"[-] Warning: Cover image file not resolved on disk for: {shortcode}")

            try:
                # 2. Call Decoupled LLM Extractor
                extracted = extractor.extract_competition_details(raw_post.raw_caption, img)

                # 3. Call Decoupled Persistence Adapter to save in safe sub-transaction boundary
                CompetitionRepository.save_extracted_competition(db, raw_post, extracted)
                db.commit()

                pipeline_tracker.complete_post(success=True)
                print(f"[+] Successfully extracted and saved competition details for: {shortcode}")

            except Exception as e:
                db.rollback()
                error_msg = f"Failed to process {shortcode}: {str(e)}"
                pipeline_tracker.complete_post(success=False, error_msg=error_msg)
                print(f"[-] Failure: {error_msg}")
    finally:
        pipeline_tracker.finish()

    print("[*] Multimodal LLM Extraction Pipeline finished.")
