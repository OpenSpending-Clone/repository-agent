FROM python:3.6-alpine

RUN apk add --update --no-cache \
    git

ADD . /app

RUN apk add --virtual .build-deps \
    gcc \
    python3-dev \
    && pip install -e ./app \
    && apk del --no-cache .build-deps

# ENV repos list

WORKDIR /app/datapackage_pipelines_registry_agent

ENTRYPOINT ["celery"]
CMD ["-A", "scheduler", "worker", "-B"]
