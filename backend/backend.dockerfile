FROM tiangolo/uvicorn-gunicorn:python3.9 as base

FROM base as builder

WORKDIR /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-server-dev-all python3-dev autoconf automake g++ make \
    libffi-dev libxml2-dev libxslt-dev libssl-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir "cryptography==3.3" poetry pipenv\
 && poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN sh -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

RUN pip uninstall --yes poetry

FROM builder
WORKDIR /app/

COPY --from=builder /usr/local /usr/local

COPY ./app /app
ENV PYTHONPATH=/app