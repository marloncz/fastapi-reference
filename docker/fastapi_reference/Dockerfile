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

# NOTE: Not needed for local SQLite database
# Install Microsoft ODBC Driver for SQL Server
# ADD https://packages.microsoft.com/keys/microsoft.asc /tmp/microsoft.asc
# ADD https://packages.microsoft.com/config/debian/11/prod.list /etc/apt/sources.list.d/mssql-release.list

# RUN cat /tmp/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc && \
#     rm /tmp/microsoft.asc && \
#     apt update && \
#     apt -y upgrade && \
#     ACCEPT_EULA=Y apt install -y unixodbc msodbcsql18 && \
#     rm -rf /var/lib/apt/lists/*

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

COPY /src /app
# NOT: only for local SQLite database and just for showcase
COPY /database /app

# Copy virtual environment with app and dependencies
COPY --from=builder /venv /venv

# Activate virtual environment
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set workdir
WORKDIR /app

# Expose REST API (runs on port 8000)
EXPOSE 8000

# command for running the API
CMD ["uvicorn", "fastapi_reference.service.api:app", "--host", "0.0.0.0", "--port", "8000"]
