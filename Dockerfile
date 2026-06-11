# Stage 1
FROM python:3.14-slim AS deps

WORKDIR /bench-backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --only=main --no-root


# Stage 2
FROM python:3.14-slim AS runtime

WORKDIR /bench-backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r app && useradd -r -g app app

COPY --from=deps /bench-backend/.venv /bench-backend/.venv

ENV PATH="/bench-backend/.venv/bin:$PATH"
ENV PRODUCTION=1

COPY ./app ./app

COPY alembic.ini .
COPY alembic ./alembic

USER app

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["gunicorn", "-c", "app/gunicorn.conf.py", "app.main:app"]