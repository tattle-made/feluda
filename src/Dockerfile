# FROM jrottenberg/ffmpeg:4.0-scratch AS ffmpeg

FROM python:3.11-slim-bullseye AS base

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
RUN groupadd -g 999 python && \
    useradd --create-home -r -u 999 -g python python
RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

# Set venv
RUN python -m venv /usr/app/venv && chown -R python:python /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip
RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends vim curl
# RUN apt-get install -y ffmpeg
# RUN apt-get update && \
#     apt-get -y upgrade && \
#     apt-get install -y tesseract-ocr tesseract-ocr-hin
RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends wget
COPY --chown=python:python requirements.txt /usr/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=python:python . /usr/app
EXPOSE 7000

# RUN apt-get update \
#     && apt-get -y upgrade \
#     && apt-get purge -y --auto-remove \
#     gcc build-essential vim curl \ 
#     libgl1-mesa-glx libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/* 

#### DEBUG IMAGE ####
FROM base AS debug
RUN apt-get update && apt-get install -y --no-install-recommends vim zsh jq
RUN pip install --no-cache-dir debugpy nose2
RUN export FLASK_DEBUG=1
USER 999
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run -h 0.0.0.0 -p 5000

#### PROD IMAGE ####
FROM base AS prod
USER 999
CMD flask run --host=0.0.0.0
