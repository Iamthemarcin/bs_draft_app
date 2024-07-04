FROM python:3.12-alpine
LABEL maintainer="milczanowski.marcin01@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./bs_draft_app /bs_draft_app
COPY ./scripts /scripts

WORKDIR /bs_draft_app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home bs_draft_app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R bs_draft_app:bs_draft_app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER bs_draft_app

ENTRYPOINT ["entrypoint.sh"]

CMD ["run.sh"]