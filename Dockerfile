FROM python:3.10.5-bullseye

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app \
    POETRY_VERSION=1.5.1

RUN apt-get -qq update && apt-get -qqy upgrade \
    && apt-get install -qqy --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip3 install --upgrade pip wheel && \
    pip3 install poetry==${POETRY_VERSION} && \
    poetry install --no-interaction --no-ansi --only main

COPY . /app
