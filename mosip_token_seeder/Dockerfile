FROM python:3.8.13-alpine3.16

ADD ./requirements.txt /app/requirements.txt

RUN apk add bash
RUN cd /app; pip3 install -r requirements.txt

ARG container_user=mosip
ARG container_user_group=mosip
ARG container_user_uid=1001
ARG container_user_gid=1001

ENV TOKENSEEDER_ROOT__PID_GREP_NAME='gunicorn'
ENV TOKENSEEDER_GUNICORN__WORKERS=4
ENV TOKENSEEDER_GUNICORN__MAX_REQUESTS=10000
ENV TOKENSEEDER_GUNICORN__TIMEOUT=5
ENV TOKENSEEDER_GUNICORN__KEEP_ALIVE=5

RUN addgroup -g ${container_user_gid} ${container_user_group} \
&& adduser -h /home/${container_user} -u ${container_user_uid} -G ${container_user_group} -s /bin/bash -D ${container_user}

USER ${container_user}
ADD --chown=${container_user}:${container_user_group} . /app
WORKDIR /

CMD gunicorn \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers ${TOKENSEEDER_GUNICORN__WORKERS} \
    --bind 0.0.0.0:8080 \
    --max-requests ${TOKENSEEDER_GUNICORN__MAX_REQUESTS} \
    --timeout ${TOKENSEEDER_GUNICORN__TIMEOUT} \
    --keep-alive ${TOKENSEEDER_GUNICORN__KEEP_ALIVE} \
    app:app