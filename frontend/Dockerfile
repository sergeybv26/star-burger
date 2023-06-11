FROM python:3.10-slim

RUN apt update && apt install -y curl \
        nodejs npm \
        binutils-gold \
        g++ \
        gcc \
        gnupg \
        make \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

WORKDIR /frontend
COPY . /frontend/
RUN npm ci
