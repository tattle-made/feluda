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
RUN pip install --no-cache-dir -r requirements.txt

CMD python receive.py
# CMD tail -f /dev/null