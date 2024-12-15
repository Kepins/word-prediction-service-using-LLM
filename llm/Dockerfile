FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN set -x && \
    apt-get update && \
    apt-get install --no-install-recommends --assume-yes \
      build-essential \
      python3 \
      python3-pip \
      python3-venv \
      python3-setuptools \
      git \
      nvidia-cuda-toolkit && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create user
ARG UID=2000
ARG GID=2000
RUN set -x && \
    groupadd -g "${GID}" python && \
    useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python && \
    chown python:python -R /app

USER python

# Copy resources
COPY resources resources

RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt --no-build-isolation
RUN pip3 install flash-attn --no-build-isolation

# Copy application code
COPY src src

# Don't buffer Python output
ENV PYTHONUNBUFFERED=1

CMD ["python3", "src/main.py"]
