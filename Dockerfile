ARG GIT_COMMIT_SHA
ARG VERSION

FROM python:3.12.6-slim AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    g++ \
    build-essential \
    libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.2

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate && \
  poetry add alembic && \
  poetry lock && \
  poetry install --no-dev --no-root

COPY . .

RUN . /venv/bin/activate && poetry build

FROM python:3.12.6-alpine3.20 AS prod

# Copy build arguments
ARG GIT_COMMIT_SHA
ARG VERSION
ARG BUILD_DATE

USER root

RUN mkdir -p /usr/src/app && \
  chown -R 65534:65534 /usr/src/app && \
  chmod -R 755 /usr/src/app && \
  BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

WORKDIR /usr/src/app

COPY --from=builder --chown=65534:65534 /venv /venv
COPY --from=builder --chown=65534:65534 /app/dist .

ENV PATH="/venv/bin:$PATH" \
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONUNBUFFERED=1 \
  VERSION=$VERSION \
  GIT_COMMIT_SHA=$GIT_COMMIT_SHA \
  BUILD_DATE=$BUILD_DATE

  # make /var/logs writable
RUN mkdir -p /var/logs/smig_trader && \
  mkdir -p /.cache/pip && \
  chown -R 65534:65534 /.cache/pip && \
  chown -R 65534:65534 /var/logs/smig_trader && \
  chmod -R 755 /var/logs/smig_trader

# switch to the nobody user
USER 65534

RUN pip install *.whl

RUN rm -rf /.cache.pip/*

EXPOSE 8000

# Add labels
LABEL maintainer="Mitch Murphy" \
  org.opencontainers.image.authors="Mitchell Murphy<mitch.murphy@gmail.com>" \
  org.opencontainers.image.title="SmigTrader" \
  org.opencontainers.image.url="https://github.com/mkm29/smig_trader.git" \
  org.opencontainers.image.vendor="Smigula Developm ent" \
  org.opencontainers.image.version=$VERSION \
  org.opencontainers.image.licenses="MIT" \
  org.opencontainers.image.revision=$GIT_COMMIT_SHA \
  org.opencontainers.image.created=$BUILD_DATE

# Since the virtual environment is activated in a RUN instruction, it will not persist to the ENTRYPOINT or CMD.
ENTRYPOINT ["/bin/bash", "-c", "source /venv/bin/activate && exec $0 \"$@\"", "uvicorn"]
# CMD ["--port", "8000", "--factory", "--workers", "1", "--host", "0.0.0.0", "smig_trader.main:create_app"]
