# Project Folder Structure Guide

This document describes the role and responsibility of each directory and file in the Instagram Scraper API project:

---

## Directory Layout

```text
nyobak scrapping/
├── .env                  # Local secrets file storing the active SessionID (ignored by git)
├── .env.example          # Environment variable template for initial project setup
├── .gitignore            # Specifying untracked files/folders to ignore (media, .venv, etc.)
├── Dockerfile            # Ultra-fast containerized blueprint optimized with 'uv'
├── docker-compose.yml    # Multicontainer orchestration (FastAPI and future database services)
├── main.py               # Root bootstrapper script to execute Uvicorn
├── pyproject.toml        # Unified project metadata, uv lock, Ruff, and Mypy rules
├── README.md             # The main documentation landing page for the project
├── docs/                 # Center for deep-dive technical documentation
│   ├── architecture.md   # Architectural design, data flow, and concurrency handling
│   ├── code_standards.md # Style standards, lint rules, and type hinting conventions
│   ├── folder_structure.md # This guide (directory breakdown)
│   └── future_guidelines.md # Blueprints for Database, CRUD, and LLM integrations
├── media/                # Persistent local storage where crawled image covers are stored
│   └── [username]/       # Directories created dynamically per scraped account
│       └── [code].jpg    # Covers renamed matching their unique Instagram media shortcode
└── app/                  # Main FastAPI Application
    ├── __init__.py       # Package initialization
    ├── config.py         # Loads env configurations and prepares local folders
    ├── main.py           # Initializes FastAPI, mounts static routes, and registers API routers
    ├── api/              # API router boundary layer
    │   ├── __init__.py
    │   └── endpoints.py  # Declares routes and offloads blocking calls to worker threadpools
    ├── schemas/          # Schema validation boundaries
    │   ├── __init__.py
    │   └── post.py       # Pydantic models for predictable and secure JSON outputs
    └── services/         # Core business logic boundary layer
        ├── __init__.py   # Global services module exports
        └── instagram/    # Dedicated modular package for Instagram integrations
            ├── __init__.py
            ├── client.py # Managing client session lifecycle, proxies, and SessionID logins
            ├── exceptions.py # Houses domain-specific exceptions (InstagramRateLimitException)
            └── scraper.py # Scraping workflows, random jitter delays, and download tasks
```

---

## File Responsibilities

### Root Configuration Files
* **`main.py` (Root):** A lightweight entrypoint script which invokes Uvicorn (`uvicorn.run("app.main:app", ...)`). This allows execution of the development server via the simple command `uv run main.py`.
* **`pyproject.toml`:** The single source of truth for modern Python packaging. Defines dependency constraints, Ruff rules (linting and formatting styles), and Mypy flags for type checking.
* **`.env` & `.env.example`:** `.env.example` acts as a developer template detailing required configuration options. `.env` is a local git-ignored secret store for the browser `INSTAGRAM_SESSIONID` cookie.

### Core Source Code (`app/`)
* **`app/main.py`:** Prepares and instantiates the FastAPI engine. Mounts the local `media/` folder as a static files directory via FastAPI's `StaticFiles`. This enables persistent local access to downloaded cover files through clean local URLs (e.g., `http://localhost:8000/media/instagram/C5edaaa0.jpg`).
* **`app/config.py`:** Automates loading configuration variables from the active `.env` file. These configurations are made globally available as clean constants.
* **`app/api/endpoints.py`:** Declares the GET `/instagram/scrape` route. Implements Starlette's worker threadpool tool (`run_in_threadpool`) to safely execute synchronous blocking Instagrapi scraper calls without blocking FastAPI.
* **`app/services/instagram/client.py`:** Connects to Instagram through a residential proxy (if defined). Authenticates utilizing the browser's tepercaya `sessionid` cookie to prevent suspicious login triggers.
* **`app/services/instagram/scraper.py`:** The heart of the scraping sequence. Handles user resolution, media fetching, random jitter execution, photo cover downloads, and structured output formatting.
