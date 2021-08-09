FROM jrottenberg/ffmpeg:4.0-scratch AS ffmpeg

FROM python:3.7-slim AS server_base
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

# RUN apt-get update \
#     && apt-get -y upgrade \
#     && apt-get purge -y --auto-remove \
#     gcc build-essential vim curl \ 
#     libgl1-mesa-glx libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/* 


EXPOSE 7000
# CMD python application.py
CMD tail -f /dev/null