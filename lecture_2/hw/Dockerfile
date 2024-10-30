FROM python:3.12 AS base

ARG PYTHONFAULTHANDLER=1
ARG    PYTHONUNBUFFERED=1
ARG    PYTHONHASHSEED=random
ARG    PIP_NO_CACHE_DIR=on
ARG    PIP_DISABLE_PIP_VERSION_CHECK=on
ARG    PIP_DEFAULT_TIMEOUT=500

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install --upgrade pip

WORKDIR $APP_ROOT/src
COPY ./lecture_2 ./lecture_2

ENV VIRTUAL_ENV=$APP_ROOT/src/.venv \
    PATH=$APP_ROOT/src/.venv/bin:$PATH

RUN pip install -r lecture_2/hw/requirements.txt

CMD ["uvicorn", "lecture_2.hw.shop_api.main:app", "--port", "8080", "--host", "0.0.0.0"]
