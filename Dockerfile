# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /app

# ---- Dependencies ----------------------------------------------------------
FROM base AS deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime -----------------------------------------------------------------
FROM base AS runtime
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY --chown=appuser:appuser . ./

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request, os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\", 3000)}/health')" || exit 1

CMD ["python", "-m", "src.server"]
