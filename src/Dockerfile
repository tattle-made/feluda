# FROM jrottenberg/ffmpeg:4.0-scratch AS ffmpeg

FROM --platform=$TARGETPLATFORM python:3.11-slim-bullseye@sha256:47863f26a5f2e0bfa903e7b658355940250979bd555b5e4f9f25da81647daff8 AS base
ARG UID
ARG GID

# COPY --from=ffmpeg / /
RUN apt-get update \
    && apt-get -y upgrade \
#    && apt-get install -y \
#    --no-install-recommends gcc build-essential \
#    --no-install-recommends libgl1-mesa-glx libglib2.0-0 \
#    && apt-get purge -y --auto-remove \
#    gcc build-essential \
#    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set python user
RUN groupadd -f -g $GID python \
    && id -u python >/dev/null 2>&1 || useradd --create-home -r -u $UID -g python python \
    && mkdir -p /usr/app \
    && chown -R python:python /usr/app
WORKDIR /usr/app

# Set venv
RUN python -m venv /usr/app/venv && chown -R python:python /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

# base requirements file
COPY --chown=python:python base_requirements.txt /usr/app/base_requirements.txt
RUN pip install --no-cache-dir --require-hashes --no-deps -r /usr/app/base_requirements.txt

RUN apt-get update --fix-missing && apt-get -y upgrade && apt-get install -y --no-install-recommends vim curl ffmpeg
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-hin tesseract-ocr-tam tesseract-ocr-tel
RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends wget
COPY --chown=python:python requirements.txt /usr/app/requirements.txt
RUN pip install --no-cache-dir --require-hashes --no-deps -r requirements.txt
COPY --chown=python:python . /usr/app

EXPOSE 7000
EXPOSE 8888

# RUN apt-get update \
#     && apt-get -y upgrade \
#     && apt-get purge -y --auto-remove \
#     gcc build-essential vim curl \
#     libgl1-mesa-glx libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

#### DEBUG IMAGE ####
FROM base AS debug
ARG UID
ARG GID

RUN apt-get update && apt-get install -y --no-install-recommends vim zsh jq

# Set python user
RUN groupadd -f -g $GID python \
    && id -u python >/dev/null 2>&1 || useradd --create-home -r -u $UID -g python python \
    && mkdir -p /usr/app \
    && chown -R python:python /usr/app
WORKDIR /usr/app

# Set venv path
ENV PATH="/usr/app/venv/bin:$PATH"

# dev requirements file
COPY --chown=python:python dev_requirements.txt /usr/app/dev_requirements.txt
RUN pip install --no-cache-dir --require-hashes --no-deps -r /usr/app/dev_requirements.txt

# Set unprivileged user with group membership
USER python:python

CMD python -m debugpy --listen localhost:5678 --wait-for-client -m flask run --debug -h localhost -p 5000

#### PROD IMAGE ####
# TODO: Setup production WSGI server - https://flask.palletsprojects.com/en/3.0.x/deploying/index.html
#FROM base AS prod
#USER python:python
#CMD flask run --host=0.0.0.0
