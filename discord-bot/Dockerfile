FROM python:3.9-alpine
LABEL maintainer="reyland.dev"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt \
     ./bot-entrypoint.sh \
     /

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    chmod +x /bot-entrypoint.sh && \
    adduser --disabled-password --no-create-home app

COPY ./config.yml ./bot.py /app/
COPY ./cogs /app/cogs

WORKDIR /app

ENV PATH="/py/bin:$PATH"

CMD [ "/bot-entrypoint.sh" ]

