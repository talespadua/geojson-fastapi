# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=.

# Set work directory
WORKDIR /code

# Install dependencies manager
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copy dependencies and install them
COPY poetry.lock pyproject.toml Makefile mypy.ini /code/
RUN poetry install --no-interaction --no-root

# Copy source code
COPY project /code/project
