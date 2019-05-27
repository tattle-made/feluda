FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

#RUN mkdir -p /var/data/models

EXPOSE 5000

CMD gunicorn --preload -w 2 --threads 1 --bind 0.0.0.0:5000 application:application
# CMD python application.py
