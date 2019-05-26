FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip3 \
    && apt-get clean

COPY . /app

RUN pip3 install -U pip3

WORKDIR /app

COPY pip-conf/pip.conf /root/.pip/
COPY pip-conf/.pypirc /root

RUN pip-compile requirements.in
RUN pip3 install -r requirements.txt

#RUN mkdir -p /var/data/models

EXPOSE 5000

CMD gunicorn --preload -w 2 --threads 1 --bind 0.0.0.0:5000 application:application
# CMD python application.py
