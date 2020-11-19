FROM python:3.7-slim as builder

RUN apt-get update \
&& apt-get -y upgrade \
&& apt-get install -y \
    --no-install-recommends gcc build-essential \
    --no-install-recommends libgl1-mesa-glx libglib2.0-0 \
    # Vim is only for debugging in dev mode. Uncomment in production
    vim \
&& apt-get purge -y --auto-remove \
    gcc build-essential \
    libgl1-mesa-glx libglib2.0-0 \
&& rm -rf /var/lib/apt/lists/* 

RUN pip install --upgrade pip

# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install pip-tools
# COPY requirements.in /app/requirements.in
COPY requirements.txt /app/requirements.txt
WORKDIR /app
# RUN pip-compile requirements.in
RUN pip install --user -r requirements.txt

FROM jrottenberg/ffmpeg:4.0-scratch AS ffmpeg

FROM python:3.7-slim AS indexer_prod
COPY --from=ffmpeg / /
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

CMD python receive.py
# CMD tail -f /dev/null