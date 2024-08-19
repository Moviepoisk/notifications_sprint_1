#!/bin/bash

while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
      echo "Waiting $REDIS_HOST"
      sleep 1
done


if [[ "$DEBUG" = "True" ]]
then
  uvicorn app.main:app --host "$WS_SERVICE_HOST" --port "$WS_SERVICE_PORT" --reload --workers "$WS_SERVICE_WORKERS" --log-level "$WS_SERVICE_LOG_LEVEL"
else
  gunicorn app.main:app --bind  "$WS_SERVICE_HOST:$WS_SERVICE_PORT" --workers "$WS_SERVICE_WORKERS" --log-level "$WS_SERVICE_LOG_LEVEL" -k uvicorn.workers.UvicornWorker
fi
