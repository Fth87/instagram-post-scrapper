# Instagram Scraper API (Production Grade)

A production-ready Instagram scraper built with FastAPI (Clean Architecture) and Instagrapi (Private Mobile API). This system is designed to crawl public Instagram accounts, download covers, and serve them locally to prepare clean, structured inputs for multimodal LLM pipelines (e.g. Gemini AI).

The scraper implements advanced anti-bot safety mechanisms including Residential Proxy Routing, Human-like Jitter Delays, and Browser SessionID Cookie Bypass to prevent rate limits and security challenges.

---

## Key Features

*   **FastAPI Clean Architecture:** Clean separation of concerns between presentation routing (`api`), validation models (`schemas`), and business logic (`services`).
*   **100% Bypass Checkpoint (SessionID Bypass):** Skips suspicious password login requests and authenticates utilizing active browser session cookies.
*   **Residential Proxy Routing:** Runs traffic through rotating residential proxies before logging in to protect local IP addresses.
*   **Human-like Jitter:** Random delays (5.0 to 15.0 seconds) inserted dynamically after API requests to replicate human surfing patterns.
*   **Persistent Local Storage:** Downloads cover media locally, renames them matching their unique shortcode, and serves them persistently as static files (e.g., `http://localhost:8000/media/...`).
*   **Docker and uv Ready:** Includes a clean Dockerfile optimized with Astral's ultra-fast package manager 'uv'.

---

## Directory Structure

```text
nyobak scrapping/
├── app/                  # Main FastAPI Application
│   ├── api/              # API endpoints and worker threadpool offloading
│   ├── schemas/          # Input/output schemas via Pydantic
│   └── services/         # Business logic (modular Instagram services package)
├── docs/                 # Developer Documentation Center
│   ├── architecture.md   # Architectural design, data flow, and concurrency handling
│   ├── folder_structure.md # Role and responsibility of folders/files
│   ├── code_standards.md # Style conventions, Ruff linter, and Mypy
│   └── future_guidelines.md # Blueprints for Database, CRUD, and LLM pipelines
├── media/                # Persistent local storage where scraped covers are saved
├── Dockerfile            # Containerization blueprint
├── docker-compose.yml    # Multicontainer docker orchestration
└── pyproject.toml        # Unified project dependency locking and lint rules
```

> [!NOTE]
> Detailed technical guides, flowcharts, and styling rules are available inside the **[docs/](file:///mnt/data/lomba/info%20mazze/IYT/nyobak%20scrapping/docs/)** folder.

---

## Quick Start

### Prerequisites
Make sure that Astral's modern package manager **uv** is installed on your operating system. If not, install it using the following commands:
```bash
# For Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# For Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### Step 1: Set Up Environment Configuration File (.env)
Copy the `.env.example` file to `.env` in the root workspace directory:
```bash
cp .env.example .env
```

Open the newly created **[`.env`](file:///mnt/data/lomba/info%20mazze/IYT/nyobak%20scrapping/.env)** file and fill in the parameters:

```env
# Copy the value of the 'sessionid' cookie from instagram.com after logging in
INSTAGRAM_SESSIONID=your_sessionid_cookie_value_here

# Residential Proxy URL (Format: http://username:password@ip:port)
RESIDENTIAL_PROXY_URL=http://lfkyzkdp:5o0725zgwfem@38.154.203.95:5863

# Gemini API Key (Optional - for future LLM analysis phase)
GEMINI_API_KEY=
```

> [!TIP]
> **How to extract 'sessionid':** Open instagram.com -> Login -> Press F12 to open Developer Tools -> Go to the **Application** tab (or **Storage** in Firefox) -> Expand **Cookies** -> Click on instagram.com -> Find the cookie named **`sessionid`** and copy its value.

---

### Step 2: Start the FastAPI Server

Execute the bootstrapper script to automatically provision the virtual environment, install dependencies, and run the development server:

```bash
uv run main.py
```

Your API server will start running at **`http://localhost:8000`**!

---

### Step 3: Access Swagger UI and Crawl

1. Open your web browser and go to the interactive documentation:
   🔗 **`http://localhost:8000/docs`**
2. Locate the **`GET /instagram/scrape`** endpoint.
3. Click the **"Try it out"** button.
4. Input the query parameters:
   * `username`: A public Instagram username (e.g., `infolomba`).
   * `limit`: The number of recent post covers to fetch (range: 1 to 20).
5. Click **"Execute"**.

FastAPI will fetch the public account, resolve metadata, download cover photos locally to the `media/` directory, and return a clean, structured JSON response with static persistent image URLs.

---

## Production Deployment with Docker

To deploy the application in a persistent production environment:

```bash
# Build and start container services in the background
docker compose up -d --build
```
Your FastAPI application will now be running on port `8000` inside a highly optimized, isolated Docker container.

---

## Technical Developer Documentation

To understand the core design and start extending the project:

1. **[docs/architecture.md](file:///mnt/data/lomba/info%20mazze/IYT/nyobak%20scrapping/docs/architecture.md)** — Architectural design, flow of control, Dependency Injection, and threadpool handling.
2. **[docs/folder_structure.md](file:///mnt/data/lomba/info%20mazze/IYT/nyobak%20scrapping/docs/folder_structure.md)** — Rationale and purpose of every directory and file.
3. **[docs/code_standards.md](file:///mnt/data/lomba/info%20mazze/IYT/nyobak%20scrapping/docs/code_standards.md)** — Naming rules, Python PEP-8 coding styles, Ruff linter configurations, and Mypy static checks.
4. **[docs/future_guidelines.md](file:///mnt/data/lomba/info%20mazze/IYT/nyobak%20scrapping/docs/future_guidelines.md)** — Blueprints and template implementations for SQLModel/Alembic databases and Google Gemini multimodal LLM analysis.
