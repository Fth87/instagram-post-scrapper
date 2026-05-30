from sqlmodel import SQLModel, create_engine, Session
from app.config import BASE_DIR

# Establish database storage filepath inside the project root
SQLITE_FILE = BASE_DIR / "instagram_scraper.db"
sqlite_url = f"sqlite:///{SQLITE_FILE}"

# Configure SQLAlchemy engine for SQLite, safe for multi-threaded environments like FastAPI
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False}
)

def get_db():
    """
    Dependency generator yielding database sessions.
    Ensures safe transaction lifecycles and clean connection closure.
    """
    with Session(engine) as session:
        yield session

def init_db() -> None:
    """
    Creates all SQLite database tables statically on application startup
    if they do not already exist.
    """
    # Import all models to ensure SQLModel registers their metadata schema
    from app.models import (  # noqa: F401
        RawInstagramPost,
        Competition,
        CompetitionTimeline,
        CompetitionCategory,
    )
    
    print("[*] Initializing SQLite database tables...")
    SQLModel.metadata.create_all(engine)
    print("[+] Database tables initialized successfully.")
