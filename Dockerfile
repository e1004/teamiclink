# STEP
FROM python:3.9-buster as normal_start
RUN apt-get update -y && \
    apt-get install libpq-dev=11.9-0+deb10u1 -y

# STEP
FROM python:3.9-slim-buster as slim_start
RUN apt-get update -y && \
    apt-get install libpq5=11.9-0+deb10u1 -y

# STEP
FROM normal_start as base
WORKDIR /tmp
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN python -m pip install --upgrade --no-cache-dir pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# STEP
FROM slim_start as result
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
RUN groupadd -g 61000 docker && \
    useradd -g 61000 -l -M -s /bin/false -u 61000 docker
COPY --from=base --chown=docker:docker /opt/venv /opt/venv
COPY --chown=docker:docker gunicorn.ini.py teamiclink/ ./teamiclink/
USER docker
