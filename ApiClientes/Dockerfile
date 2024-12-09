FROM python:3.10-slim AS builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.10-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . ./app
WORKDIR /app/
EXPOSE 8080

RUN python manage.py collectstatic --noinput

ENV REDIS_TESTING=False
ENV PYTHONUNBUFFERED=1
ENV INIT=True
ENTRYPOINT ["gunicorn", "-w", "4", "ApiClientes.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level=debug"]


FROM caddy:2.8.4-alpine AS caddy-runtime
COPY --from=runtime /app/static /srv/static/

