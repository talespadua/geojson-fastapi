FROM python:3.8.5-alpine3.12 AS base
WORKDIR /app/

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

COPY poetry.lock pyproject.toml ./
RUN apk add --no-cache mariadb-connector-c-dev && \
    apk add --no-cache --virtual .build-deps mariadb-dev gcc python3-dev musl-dev libffi-dev openssl-dev make && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root && \
    pip uninstall poetry -y && \
    apk del .build-deps
COPY . .