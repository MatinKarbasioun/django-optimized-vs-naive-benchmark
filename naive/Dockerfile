ARG PYTHON_VERSION=3.13.5
FROM python:${PYTHON_VERSION}-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-chache-dir -r requirements.txt


FROM python:${PYTHON_VERSION}-slim

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser


USER appuser

COPY . .

ENTRYPOINT exec pre_startup.sh

EXPOSE 8000

# Run the application.
CMD gunicorn 'crm_naive.wsgi':application --bind 0.0.0.0:8000 --workers 2 --threads 4 --worker-class gthread
