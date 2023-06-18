###############################################
# Base Stage
###############################################
FROM python:3.10-slim as base

ARG SECRET_KEY \
    ALLOWED_HOSTS \
    DEBUG \
    YA_GEO_API_KEY \
    DB_URL \
    ROLLBAR_TOKEN \
    ROLLBAR_ENVIRONMENT

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    SECRET_KEY=${SECRET_KEY:-"secret_key_change_me"} \
    ALLOWED_HOSTS=${ALLOWED_HOSTS:-"localhost,127.0.0.1"} \
    DEBUG=${DEBUG:-"False"} \
    YA_GEO_API_KEY=${YA_GEO_API_KEY} \
    DB_URL=${DB_URL} \
    ROLLBAR_TOKEN=${ROLLBAR_TOKEN} \
    ROLLBAR_ENVIRONMENT=${ROLLBAR_ENVIRONMENT:-"prodaction"}

###############################################
# Build Stage
###############################################
FROM base as build

WORKDIR /backend
COPY requirements.txt /backend/
RUN apt update && apt install -y python3-pip libpq-dev                        \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

###############################################
# Development Stage
###############################################
FROM build as develop

COPY . /backend/
