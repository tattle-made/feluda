FROM jrottenberg/ffmpeg:4.0-scratch AS ffmpeg

FROM python:3.7-slim AS base
COPY --from=ffmpeg / /
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y \
    --no-install-recommends gcc build-essential \
    --no-install-recommends libgl1-mesa-glx libglib2.0-0 \
    && apt-get purge -y --auto-remove \
    gcc build-essential \
    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* 
ENV PATH=/root/.local/bin:$PATH
RUN pip install --upgrade pip
RUN pip install pip-tools
RUN apt-get update && apt-get -y upgrade && apt-get install -y vim curl
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --user -r requirements.txt
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
RUN pip install debugpy nose2
RUN export FLASK_ENV=development
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run -h 0.0.0.0 -p 5000

#### PROD IMAGE ####
FROM base as prod
CMD flask run --host=0.0.0.0