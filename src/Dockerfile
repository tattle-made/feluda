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
ENV PATH=/root/.local/bin:$PATH
RUN pip install --no-cache-dir --upgrade pip
RUN apt-get update && apt-get -y upgrade && apt-get install -y vim curl
# RUN apt-get install -y ffmpeg
# RUN apt-get update && \
#     apt-get -y upgrade && \
#     apt-get install -y tesseract-ocr tesseract-ocr-hin
RUN apt-get update && apt-get -y upgrade && apt-get install wget
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
COPY . /app
EXPOSE 7000

# RUN apt-get update \
#     && apt-get -y upgrade \
#     && apt-get purge -y --auto-remove \
#     gcc build-essential vim curl \ 
#     libgl1-mesa-glx libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/* 

#### DEBUG IMAGE ####
FROM base AS debug
RUN apt-get update && apt-get install -y vim zsh jq
RUN pip install --no-cache-dir debugpy nose2
RUN export FLASK_DEBUG=1
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run -h 0.0.0.0 -p 5000

#### PROD IMAGE ####
FROM base as prod
CMD flask run --host=0.0.0.0