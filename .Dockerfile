FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# DEFAULT DEBUG
ARG DEBUG=1

WORKDIR /app

COPY requirements /app/requirements

RUN if [ "$DEBUG" = "1" ]; then \
    pip install --no-cache-dir -r /app/requirements/development.txt; \
    else \
    pip install --no-cache-dir -r /app/requirements/production.txt; \
    fi

COPY . /app
