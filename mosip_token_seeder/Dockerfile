FROM python:3.8.13-slim-bullseye

ADD ./requirements.txt /app/requirements.txt

RUN cd /app; pip3 install -r requirements.txt

ARG container_user=mosip
ARG container_user_group=mosip
ARG container_user_uid=1001
ARG container_user_gid=1001

RUN groupadd -g ${container_user_gid} ${container_user_group} \
&& useradd -mN -u ${container_user_uid} -G ${container_user_group} -s /bin/bash ${container_user}

USER ${container_user}
ADD --chown=${container_user}:${container_user_group} . /app
WORKDIR /

ENV TOKENSEEDER_ROOT__PID_GREP_NAME='gunicorn'
ENV TOKENSEEDER_GUNICORN__WORKERS=4
ENV TOKENSEEDER_GUNICORN__MAX_REQUESTS=10000
ENV TOKENSEEDER_GUNICORN__TIMEOUT=5
ENV TOKENSEEDER_GUNICORN__KEEP_ALIVE=5

CMD gunicorn \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers ${TOKENSEEDER_GUNICORN__WORKERS} \
    --bind 0.0.0.0:8080 \
    --max-requests ${TOKENSEEDER_GUNICORN__MAX_REQUESTS} \
    --timeout ${TOKENSEEDER_GUNICORN__TIMEOUT} \
    --keep-alive ${TOKENSEEDER_GUNICORN__KEEP_ALIVE} \
    --access-logformat "${TOKENSEEDER_GUNICORN__ACCESSLOG_FORMAT}" \
    --access-logfile "-" \
    --error-logfile "-" \
    app:app