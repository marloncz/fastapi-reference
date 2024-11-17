### Base Image
FROM python:3.11.9-slim-bookworm AS base

# Python settings
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# Update system libraries
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

### Build Image
FROM base AS builder

# Install python development dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Python settings
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.2

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION" poetry-plugin-export

# Create virtual environment
RUN python -m venv /venv

# Install dependencies into virtual environment
COPY pyproject.toml poetry.lock ./
RUN poetry export --no-ansi --no-interaction --only main --without-hashes --format requirements.txt | /venv/bin/pip install -r /dev/stdin

# Install app
COPY . .
RUN poetry build --no-ansi --no-interaction --format wheel && /venv/bin/pip install dist/*.whl

### Final Image
FROM base AS final

# Copy virtual environment with app and dependencies
COPY --from=builder /venv /venv

# Activate virtual environment
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Login as non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser
