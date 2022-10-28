FROM python:3.9.15-alpine

LABEL description="Kubernetes OpenShift Console operator"

ENV APPDIR /app
ENV PYTHONUNBUFFERED 1
RUN mkdir $APPDIR
WORKDIR $APPDIR

COPY requirements.txt /tmp/
# hadolint ignore=DL3018
RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc python3-dev py-configobj linux-headers libc-dev \
    && pip install  --use-deprecated=legacy-resolver --no-cache-dir -r /tmp/requirements.txt \
    && addgroup -S app_grp && adduser -S app -G app_grp \
    && chown -R app:app_grp $APPDIR \
    && apk del .build-deps  \
    && rm -rf /var/cache/apk/*  \
    && rm -rf  /tmp/*

COPY --chown=app:app_grp . .
USER app
CMD ["kopf", "run", "-A", "--standalone", "/app/main.py"]
