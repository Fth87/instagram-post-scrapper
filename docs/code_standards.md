# Code Standards and Style Guidelines

To keep the codebase of the Instagram Scraper API clean, readable, highly consistent, and maintainable, all developers must adhere to the styling and type-safety rules detailed below.

---

## Coding Style and Naming Conventions

This project strictly follows the official Python styling standard (**PEP 8**) with modern configurations:

### 1. Variables, Functions, and Module Files (Snake Case)
* All function names, method names, local variables, filenames, and directory modules must be written in lowercase with words separated by underscores:
  * **Correct:** `instagram_service.py`, `scrape_latest_posts_sync()`, `user_id`
  * **Incorrect:** `instagramService.py`, `ScrapeLatestPosts()`, `userID`

### 2. Classes (Pascal Case)
* Class names must be written in camel case with the first letter of each word capitalized:
  * **Correct:** `InstagramScraperService`, `InstagramClientManager`
  * **Incorrect:** `instagram_scraper_service`, `Instagram_Client_Manager`

### 3. Global Constants (Upper Case)
* Global constant variables and environment-loaded configuration constants must be written in capital letters separated by underscores:
  * **Correct:** `MEDIA_DIR`, `INSTAGRAM_SESSIONID`
  * **Incorrect:** `media_dir`, `instagram_sessionid`

---

## Type Hinting Standards

All new functions, helper utilities, and service classes must include precise **Type Hints** for all arguments and return values. This ensures that static type checkers can identify type mismatches before execution:

```python
# Correct type-hinted service signature example:
def scrape_latest_posts_sync(self, username: str, limit: int, base_url: str) -> list[dict]:
    # ...
    return scraped_posts
```

---

## Code Quality Tools (Ruff and Mypy)

The project includes pre-configured tools in `pyproject.toml` to automatically check and maintain code quality:

### 1. Linter and Formatter: Ruff
* **Ruff** checks the codebase for syntax issues, styling errors, dead code, and unused imports, and automatically reformats files.
* **To check code:** 
  ```bash
  uv run ruff check
  ```
* **To auto-fix issues:**
  ```bash
  uv run ruff check --fix
  ```

### 2. Static Type Checker: Mypy
* **Mypy** checks the type annotations in the codebase statically to ensure all variables and parameters remain type-safe.
* **To check types:**
  ```bash
  uv run mypy app
  ```

---

## Core Guidelines

* **Write Docstrings:** All new service classes, endpoints, schemas, and helper methods must contain a clear, concise PEP-257 docstring using triple quotes (`"""`) to document the purpose of the code.
* **Avoid Comment Placeholders:** Do not write comments explaining obvious code blocks (avoid over-commenting). Write comments only to clarify highly complex or non-obvious design choices.
* **No Hardcoding:** Always store sensitive parameters (API Keys, secrets, passwords) in the `.env` file and access them through `app/config.py`. Never hardcode raw secret strings directly in your source code files.
