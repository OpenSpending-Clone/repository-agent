FROM python:3.6-alpine

RUN apk add --update --no-cache \
    git

ADD . /app

RUN apk add --virtual .build-deps \
    gcc \
    python3-dev \
    && mv ./app/gitconfig_for_container ~/.gitconfig \
    && pip install -e ./app \
    && apk del --no-cache .build-deps

WORKDIR /app/repository_agent

ENTRYPOINT ["celery"]
CMD ["-A", "scheduler", "worker", "-B"]
