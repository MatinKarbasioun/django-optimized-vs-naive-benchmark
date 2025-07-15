ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

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

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

RUN mkdir staticfiles

USER appuser

# Expose the application port
EXPOSE 8000
