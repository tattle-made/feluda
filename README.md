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

http://localhost:7000/media : Receives image URLs / video URLs / text documents via POST requests and sends them to a RabbitMQ job queue. This queue is consumed by `receive.py` and the processed data is indexed into the appropriate Elasticsearch index. This endpoint is designed for fault-tolerant batch indexing.  

http://localhost:7000/upload_image : Receives an image URL via a POST request and indexes it in the appropriate Elasticsearch index.   

http://localhost:7000/upload_video : Receives a video URL via a POST request and indexes it in the appropriate Elasticsearch index.   

http://localhost:7000/upload_text : Receives a text document via a POST request and indexes it in the appropriate Elasticsearch index.  

The `/upload_image`, `/upload_video` and `/upload_text` endpoints index data directly (bypassing RabbitMQ) and are suitable for development / testing.  

http://localhost:7000/search : Receives a query image / video / text and returns the top 3 matches found in the Elasticsearch index in descending order.   
Note: A text search returns two sets of matches: `simple_text_matches` and `text_vector_matches`. The former is useful for same-language search and the latter for multilingual search.  

#### Examples

```
curl --location --request POST 'http://localhost:7000/upload_text' \
--header 'Content-Type: application/json' \
--data-raw '{"source_id": "123",
"media_type": "text",
"source": "A",
"text": "Symptoms of COVID-19 are variable, but often include fever, cough, fatigue, breathing difficulties, and loss of smell and taste. Symptoms begin one to fourteen days after exposure to the virus. Around one in five infected individuals do not develop any symptoms.",
"metadata": {"test": "text indexing"}}'
```

```
curl --location --request POST 'http://localhost:7000/upload_image' \
--header 'Content-Type: application/json' \
--data-raw '{"source_id": "456",
  "media_type": "image",
  "source": "B",
  "image_url": "https://tattle-story-scraper.s3.ap-south-1.amazonaws.com/e9ec45b7-3e9a-46a2-ba8e-46e606b85da6",
  "metadata": {"test": "image indexing"}
} '

```

```
curl --location --request POST 'http://localhost:7000/search' \
--header 'Content-Type: application/json' \
--data-raw '{"source_id": "123",
"media_type": "text",
"source": "A",
"text": "कोविड-19 के लक्षण परिवर्तनशील हैं, लेकिन अक्सर बुखार, खांसी, थकान, सांस लेने में कठिनाई और गंध और स्वाद की हानि शामिल हैं। वायरस के संपर्क में आने के एक से चौदह दिन बाद लक्षण दिखाई देने लगते हैं। पांच में से एक संक्रमित व्यक्ति में कोई लक्षण विकसित नहीं होते हैं।",
"metadata": {"test": "text search"}}'
```
