FROM python:3.11-slim-bookworm as builder

WORKDIR /opt

COPY ./app/requirements.txt ./app/requirements.txt

RUN apt-get update  \
    && apt install netcat-traditional  \
    && pip install --upgrade pip  \
    && pip install -r ./app/requirements.txt --no-cache-dir


FROM builder

COPY ./app ./app
COPY ./entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
