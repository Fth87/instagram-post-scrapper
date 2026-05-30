# ==============================================================================
# Production Dockerfile using Astral's uv for ultra-fast, lightweight builds
# ==============================================================================

# 1. Use the official Python slim image for a small container footprint
FROM python:3.12-slim AS builder

# 2. Install uv inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set the environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 4. Set working directory
WORKDIR /app

# 5. Copy configuration and lockfiles first to leverage Docker caching
COPY pyproject.toml uv.lock ./

# 6. Install dependencies into a virtual environment
# We omit installing the project itself first to cache dependencies successfully
RUN uv sync --frozen --no-install-project --no-dev

# 7. Copy the rest of the source code
COPY . .

# 8. Re-run sync to install the project itself
RUN uv sync --frozen --no-dev

# 9. Expose FastAPI default port
EXPOSE 8000

# 10. Start the server using the compiled virtual environment
CMD ["uv", "run", "main.py"]
