FROM python:3.7-slim

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y --no-install-recommends gcc build-essential 
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0

# This is only for debugging in dev mode. Uncomment in production
RUN apt-get install -y vim

RUN pip install --upgrade pip
RUN pip install pip-tools
RUN pip-compile requirements.in
RUN pip install --no-cache-dir -r requirements.txt

#RUN mkdir -p /var/data/models

EXPOSE 7000

# CMD gunicorn --preload -w 2 --threads 1 --bind 0.0.0.0:5000 application:application
# CMD python application.py
CMD tail -f /dev/null
