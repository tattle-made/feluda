# Feluda

A configurable multimedia and multi modal search engine.
This forms the core of our search services. Since different use cases might require different search capabilities with different trade offs, Tattle Search lets you specify which building blocks you want to use for the purpose and spins a search engine with a corresponding configuration.

## Features
- Support for Vector based embeddings using ResNet models and Sentence Transformers
- Support for hash based search using pHash

## Contributing
Please create a new Discussion [here](https://github.com/tattle-made/tattle-api/discussions) describing what you'd like to do and we'll follow up. 


## Setup for Developing Locally

1. Set environment variables by replacing the credentials in `/src/indexer/.env-template` and `/src/api-server/.env-template` with your credentials. Rename the files to `.env` and `.env` respectively.
   (For production, update the RabbitMQ and Elasticsearch host and credentials in the `.env` files)

2. Run `docker-compose up` . This will bring up the following containers:

Elasticsearch : Used to store searchable representations of multilingual text, images and videos.

RabbitMQ : Used as a Job Queue to queue up long indexing jobs.

Search Indexer : A RabbitMQ consumer that receives any new jobs that are added to the queue and processes them.

Search Server : A public REST API to index new media and provide additional public APIs to interact with this service.

The first time you run `docker-compose up` it will take several minutes for all services to come up. Its usually instantaneous after that, as long as you don't make changes to the Dockerfile associated with each service.

3. To verify if every service is up, visit the following URLs:

elasticsearch : visit http://localhost:9200

rabbitmq UI : visit http://localhost:15672

search server : visit http://localhost:5000

4. Then start the server and indexer with:

```
docker exec -it search_api python application.py
docker exec -it search_indexer python receive.py
```

#### Server endpoints

http://localhost:7000/media : Receives image URLs / video URLs / text documents via POST requests and sends them to a RabbitMQ job queue. This queue is consumed by `receive.py` and the processed data is indexed into the appropriate Elasticsearch index. This endpoint is designed for fault-tolerant bulk indexing.

http://localhost:7000/upload_image : Receives an image URL via a POST request and indexes it in the Elasticsearch image index.

http://localhost:7000/upload_video : Receives a video URL via a POST request and indexes it in the Elasticsearch video index.

http://localhost:7000/upload_text : Receives a text document via a POST request and indexes it in the Elasticsearch text index.

The `/upload_image`, `/upload_video` and `/upload_text` endpoints index data directly (bypassing RabbitMQ) and are suitable for development / testing. Indices are defined and accessed according to the names specified in `.env` and the mappings specified in `indices.py`.

http://localhost:7000/search : Receives a query image / video / text and returns the top 10 matches found in the Elasticsearch index in descending order.  
Note: A text search returns two sets of matches: `simple_text_matches` and `text_vector_matches`. The former is useful for same-language search and the latter for multilingual search.

#### Examples

```
curl --location --request POST 'http://localhost:7000/upload_text' \
--header 'Content-Type: application/json' \
--data-raw '{"source_id": "1",
"media_type": "text",
"source": "A",
"text": "Symptoms of COVID-19 are variable, but often include fever, cough, fatigue, breathing difficulties, and loss of smell and taste. Symptoms begin one to fourteen days after exposure to the virus. Around one in five infected individuals do not develop any symptoms.",
"metadata": {"test": "text indexing"}}'
```

```
curl --location --request POST 'http://localhost:7000/upload_image' \
--header 'Content-Type: application/json' \
--data-raw '{"source_id": "1",
  "media_type": "image",
  "source": "B",
  "image_url": "https://tattle-story-scraper.s3.ap-south-1.amazonaws.com/e9ec45b7-3e9a-46a2-ba8e-46e606b85da6",
  "metadata": {"test": "image indexing"}
}'

```

```
curl --location --request POST 'http://localhost:7000/search' \
--header 'Content-Type: application/json' \
--data-raw '{"source_id": "2",
"media_type": "text",
"source": "A",
"text": "कोविड-19 के लक्षण परिवर्तनशील हैं, लेकिन अक्सर बुखार, खांसी, थकान, सांस लेने में कठिनाई और गंध और स्वाद की हानि शामिल हैं। वायरस के संपर्क में आने के एक से चौदह दिन बाद लक्षण दिखाई देने लगते हैं। पांच में से एक संक्रमित व्यक्ति में कोई लक्षण विकसित नहीं होते हैं।",
"metadata": {"test": "text search"}}'
```

```
curl --location --request POST 'http://localhost:7000/upload_video' \
--header 'Content-Type: application/json' \
--data-raw '{"source_id": "2",
"media_type": "video",
"source": "B",
"file_url": "https://s3.ap-south-1.amazonaws.com/sharechat-scraper.tattle.co.in/test-videos/135f1b16_1596110374725_c_v__963e6ace-961c-41be-a28c-b3010136cedf.mp4",
"metadata": {"test": "video indexing"}}'
```

#### Bulk indexing

Bulk indexing scripts for the data collected by various Tattle services should be located in the service repository, such as [this one](https://github.com/tattle-made/sharechat-scraper/blob/development/workers/indexer/tattlesearch_indexer.py) and triggered as required. This makes the data searchable via this search API.
The indexing status of each record can be updated via a [reporter](https://github.com/tattle-made/sharechat-scraper/blob/development/workers/reporter/tattlesearch_reporter.py).  
While the former fetches data from the service's MongoDB and sends it to the API via HTTP requests, the latter is a RabbitMQ consumer that consumes reports generated by `receive.py` and adds them to the DB.

#### Dockerization

The Dockerfiles in `src/api-server` and `src/indexer` implement multistage builds to reduce image size (from approximately 5 gb each to 1.6 gb each). Since both the server and indexer have the same dependencies, it could be useful to push the first stage of their Docker builds to Dockerhub as a separate image, and then pull that image in the Dockerfiles.

Building the first stage and pushing it to a Dockerhub repository -

```
cd src/api-server
docker build --target builder -t username/repository:tag .
docker push -t username/repository:tag
```

And then replacing the following code in both the Dockerfiles -

```
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

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --user -r requirements.txt
```

with -

```
FROM username/repository:tag AS builder
```

Note that this builder image would need to be rebuilt if there is any change in the dependencies.

v : 0.0.1