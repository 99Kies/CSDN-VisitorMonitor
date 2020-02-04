FROM python:3.7-alpine

RUN apk update && \
    apk add git python3-matplotlib && \
    git pull
