from datetime import datetime
from sqlmodel import Session
from app.models.raw_post import RawInstagramPost
from app.models.competition import Competition, CompetitionTimeline, CompetitionCategory
from app.workers.pipeline.schemas import CompetitionExtraction

class CompetitionRepository:
    """
    Decoupled Persistence Adapter handling transactional SQL mappings from structured extractions.
    Uses sub-transaction boundaries (begin_nested) to safely rollback isolated failures.
    """
    @staticmethod
    def save_extracted_competition(
        db: Session, 
        raw_post: RawInstagramPost, 
        extracted: CompetitionExtraction
    ) -> None:
        with db.begin_nested():
            # 1. Create and insert the main Competition record
            competition = Competition(
                title=extracted.title,
                organizer=extracted.organizer,
                description=extracted.description,
                image_url=raw_post.image_url,
                registration_link=extracted.registration_link,
                guidebook_link=extracted.guidebook_link,
                general_contacts=extracted.general_contacts,
                instagram_shortcode=raw_post.instagram_shortcode,
                created_at=datetime.utcnow()
            )
            db.add(competition)
            db.flush()  # Populate competition ID for child FK associations

            # 2. Insert Competition Timelines
            for tl in extracted.timelines:
                try:
                    due_date = datetime.fromisoformat(tl.due_date.replace("Z", "+00:00"))
                except Exception:
                    due_date = datetime.utcnow()

                timeline = CompetitionTimeline(
                    competition_id=competition.id,
                    stage_name=tl.stage_name,
                    due_date=due_date
                )
                db.add(timeline)

            # 3. Insert Competition Categories
            for cat in extracted.categories:
                category = CompetitionCategory(
                    competition_id=competition.id,
                    name=cat.name,
                    price=float(cat.price) if cat.price is not None else 0.0,
                    contact_person=cat.contact_person
                )
                db.add(category)

            # 4. Mark raw post as processed in staging database
            raw_post.is_processed = True
            raw_post.processed_at = datetime.utcnow()
            db.add(raw_post)
