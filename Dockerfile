# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# ---- Dependencies ----------------------------------------------------------
FROM base AS deps
COPY pyproject.toml .
# Create a virtual environment and install dependencies (including dev groups)
RUN uv venv && uv sync --no-install-project

# ---- Runtime -----------------------------------------------------------------
FROM base AS runtime
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Copy the virtual environment from the deps stage
COPY --from=deps --chown=appuser:appuser /app/.venv /app/.venv

# Copy the rest of the application
COPY --chown=appuser:appuser . ./

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request, os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\", 3000)}/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
