# Installation stage
FROM python:3.11-slim AS install

WORKDIR /if_else_2024

ARG SERVER_PORT
ENV SERVER_PORT=${SERVER_PORT}

# Installing poetry
ENV POETRY_HOME=/opt/poetry
COPY install-poetry.py install-poetry.py
RUN python3 install-poetry.py --version 1.8.2

# Installing packages
COPY pyproject.toml poetry.lock ./
RUN $POETRY_HOME/bin/poetry install --no-root -n --no-cache


# Running stage
FROM install AS run

COPY ./if_else_2024 ./if_else_2024

ENTRYPOINT [ "sh", "-c", "$POETRY_HOME/bin/poetry run uvicorn --host 0.0.0.0 --port $SERVER_PORT if_else_2024.main:app" ]


# Debug stage
FROM install AS debug

RUN $POETRY_HOME/bin/poetry add debugpy

ENTRYPOINT [ "sh", "-c", "$POETRY_HOME/bin/poetry run python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m uvicorn --host 0.0.0.0 --port $SERVER_PORT --reload if_else_2024.main:app" ]
