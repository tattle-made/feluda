FROM python:3.7-slim AS builder

RUN apt-get update \
&& apt-get -y upgrade \
&& apt-get install -y \
    --no-install-recommends gcc build-essential \
    libgl1-mesa-glx libglib2.0-0 \
&& apt-get purge -y --auto-remove \
    gcc build-essential \
    libgl1-mesa-glx libglib2.0-0 \
&& rm -rf /var/lib/apt/lists/* 
# RUN apt-get install -y ffmpeg

# This is only for debugging in dev mode. Uncomment in production
RUN apt-get install -y vim

RUN pip install --upgrade pip

# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install pip-tools
# COPY requirements.in /app/requirements.in
COPY requirements.txt /app/requirements.txt
WORKDIR /app
# RUN pip-compile requirements.in
RUN pip install --user -r requirements.txt
# COPY . /app

FROM jrottenberg/ffmpeg:4.0-scratch AS ffmpeg

FROM python:3.7-slim AS server_prod
COPY --from=ffmpeg / /
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

EXPOSE 7000

# CMD python application.py
CMD tail -f /dev/null
