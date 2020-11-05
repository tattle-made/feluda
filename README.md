## Setup for Developing Locally

1. Set environment variables by replacing the credentials in /src/indexer/.env-template and /src/api-server/.env-template.local with your credentials.

2. Run `docker-compose up` . This will bring up the following containers:


Mongo DB : Used to store media hash and any associated metadata with the media.
RabbitMQ : Used as a Job Queue to queue up long media indexing jobs.
Search Indexer : A RabbitMQ consumer that receives any new jobs that are added to the queue and processes them.
Search Server : A public REST API to index new media and provide additional public APIs to interact with this service.

The first time you run docker-compose up it will take several minutes for all services to come up. Its usually instantaneous after that, as long as you don't make changes to the Dockerfile associated with each service. 

3. To verify if every service is up, visit the following URLs:

mongo : visit http://localhost:27017

rabbitmq UI : visit http://localhost:15672

search server : visit http://localhost:5000

4. Then start the server and indexer with:

```
docker exec -it search_api python application.py
docker exec -it search_indexer python receive.py
```

#### Test API calls (for direct, queue-less media indexing and search)

```
# Index an Image

curl --location --request POST 'http://localhost:7000/upload_image' \
--header 'Content-Type: application/json' \
--data-raw '{
  "image_url": "https://tattle-story-scraper.s3.ap-south-1.amazonaws.com/e9ec45b7-3e9a-46a2-ba8e-46e606b85da6",
  "doc_id": 69004
} '

# Search for Duplicate images

curl --location --request POST 'http://localhost:7000/find_duplicate' \
--header 'Content-Type: application/json' \
--data-raw '{
  "image_url": "https://tattle-story-scraper.s3.ap-south-1.amazonaws.com/e9ec45b7-3e9a-46a2-ba8e-46e606b85da6"
} '
```
