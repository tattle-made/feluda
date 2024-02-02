# Feluda

A configurable engine for analysing multi-lingual and multi-modal content.


While flexible, we built it to analyse data collected from social media - images,text and video. This forms the core of our search, clustering and analysis services. Since different use cases might require different search capabilities with different trade offs, Feluda lets you specify which building blocks you want to use for the purpose and spins an engine with a corresponding configuration.

## Example Uses
- [Khoj](https://tattle.co.in/products/khoj/) : An Reverse Image search engine to find fact check articles
- [Crowdsourcing Aid : A Case Study of the Information Chaos During India's Second Covid-19 Wave](https://tattle.co.in/articles/covid-whatsapp-public-groups/) : Analysis of whatsapp messages related to relief work collected from public whatsapp group during the second wave of Covid-19 in India.

## Understanding Operators in Feluda
When we built Feluda, we were focusing on the unique challenges of social media data that was found in India. We needed to process data in various modalities (text, audio, video, images, hybrid) and various languages. There would often be very different technologies that needed to be evaluated for each. So we built Feluda around a concept of operators. You can think of operators as plugins that you can mix and match to perform different analyses on your data (see Features section below). When you start feluda, you [configure which operators](https://github.com/tattle-made/feluda/tree/master/src/api/core/operators) you want to use and then feluda loads it. While in its current iteration Feluda comes with certain operators in its source code, the operators are defined in a way that anyone can create their own operators and use it with Feluda. Operators are easy to swap in and out. Not only does this allow you to try out various different analysis techniques, it also means you aren't tied to any one implementation for an operation. Some use cases for operators that we've tried out are following : 
1. If someone wants to run image data aggregation on a budget, instead of using an operator that uses a heavy machine learning model, they can use an operator that uses hashing instead.
2. If someone wants to extract text from images and don't want to use a google product, they could use an operator that uses openCV as opposed to google cloud vision API.
    
## Features Enabled 
- Support for Vector based embeddings using ResNet models and Sentence Transformers
- Support for hash based search using pHash
- Text extraction from images and indexing into the engine
- Entity extraction from text and images and indexing into the engine



## Contributing
Please create a new Discussion [here](https://github.com/tattle-made/tattle-api/discussions) describing what you'd like to do and we'll follow up. 

## Setup for Developing Locally

1. Set environment variables by replacing the credentials in `/src/api/.env-template` with your credentials. Rename the file to `development.env`.
   (For production, update the RabbitMQ and Elasticsearch host and credentials in the `.env` files)

  For development, replace the following in `development.env`:
  - Replace the value of `MQ_USERNAME` with the value of `RABBITMQ_DEFAULT_USER` from `docker-compose.yml`
  - Replace the value of `MQ_PASSWORD` with the value of `RABBITMQ_DEFAULT_PASS` from `docker-compose.yml`

2. Install packages for local development. These will be installed automatically with `docker compose up`

  ```
  # Install locally in venv
  $ cd src/api/
  $ pip install -r requirements.txt
  ```


3. Run `docker-compose up` . This will bring up the following containers:

  Elasticsearch : Used to store searchable representations of multilingual text, images and videos.

  RabbitMQ : Used as a Job Queue to queue up long indexing jobs.

  Search Indexer : A RabbitMQ consumer that receives any new jobs that are added to the queue and processes them.

  Search Server : A public REST API to index new media and provide additional public APIs to interact with this service.

  The first time you run `docker-compose up` it will take several minutes for all services to come up. Its usually instantaneous after that, as long as you don't make changes to the Dockerfile associated with each service.

4. To verify if every service is up, visit the following URLs:

  elasticsearch: http://localhost:9200

  rabbitmq UI: http://localhost:15672

5. Install required operators
  Each operator has to be installed separately

  ```
  # Install locally in venv
  $ cd src/api/core/operators/
  $ pip install -r image_vec_rep_resnet_requirements.txt
  $ pip install -r vid_vec_rep_resnet_requirements.txt
  ```

6. Then, in a new terminal, start the server with:
  
  ```
  $ cd src/api
  $ docker exec -it feluda_api python server.py
  ```

7. Verify that the server is running by opening: http://localhost:7000


#### Server endpoints

http://localhost:7000/media : Receives image URLs / video URLs / text documents via POST requests and sends them to a RabbitMQ job queue. This queue is consumed by `receive.py` and the processed data is indexed into the appropriate Elasticsearch index. This endpoint is designed for fault-tolerant bulk indexing.

http://localhost:7000/upload_image : Receives an image URL via a POST request and indexes it in the Elasticsearch image index.

http://localhost:7000/upload_video : Receives a video URL via a POST request and indexes it in the Elasticsearch video index.

http://localhost:7000/upload_text : Receives a text document via a POST request and indexes it in the Elasticsearch text index.

The `/upload_image`, `/upload_video` and `/upload_text` endpoints index data directly (bypassing RabbitMQ) and are suitable for development / testing. Indices are defined and accessed according to the names specified in `.env` and the mappings specified in `indices.py`.

http://localhost:7000/search : Receives a query image / video / text and returns the top 10 matches found in the Elasticsearch index in descending order.  
Note: A text search returns two sets of matches: `simple_text_matches` and `text_vector_matches`. The former is useful for same-language search and the latter for multilingual search.


#### Bulk indexing

Bulk indexing scripts for the data collected by various Tattle services should be located in the service repository, such as [this one](https://github.com/tattle-made/sharechat-scraper/blob/development/workers/indexer/tattlesearch_indexer.py) and triggered as required. This makes the data searchable via this search API.
The indexing status of each record can be updated via a [reporter](https://github.com/tattle-made/sharechat-scraper/blob/development/workers/reporter/tattlesearch_reporter.py).  
While the former fetches data from the service's MongoDB and sends it to the API via HTTP requests, the latter is a RabbitMQ consumer that consumes reports generated by `receive.py` and adds them to the DB.


#### Updating Packages

1. Update packages in `src/api/requirements.in` or operator specific requirements file:
`src/api/core/operators/<operator>_requirements.in`
2. Use `pip-compile` to generate `requirements.txt`

Note:

- Use a custom `tmp` directory to avoid memory issues
- Do not use `--generate-hashes` flag for `pip-compile` since  the cpu version of `pytorch` is being used from official repository as it is not available in `pypi`. `pip-compile` will manually generate the hash for the architecture specific file and the code will not be compatible with other architectures.
- If an operator defaults to a higher version than allowed by feluda core `requirements.txt`, manually edit the `<operator>_requirements.txt` to the compatible version. Then run `pip install`. If it runs without errors, the package version is valid for the operator.

```bash
$ cd src/api/
$ pip install --upgrade pip-tools
$ TMPDIR=<temp_dir> pip-compile --verbose --emit-index-url --emit-find-links --find-links https://download.pytorch.org/whl/torch_stable.html requirements.in

# Updating operators e.g. detect_lang_of_text
$ cd src/api/core/operators/
$ TMPDIR=<temp_dir> pip-compile --verbose --emit-index-url --emit-find-links detect_lang_of_text_requirements.in

```

#### Updating specific packages in `requirements.txt`

This is useful to update dependencies e.g. when using `pip-audit` 

```bash
$ TMPDIR=<temp_dir> pip-compile --verbose --find-links https://download.pytorch.org/whl/torch_stable.html --upgrade-package <package>==<version> --upgrade-package <package>

```

### Running Tests

To run a test, implement the following command

```bash
python -m unittest <FILE_NAME>.py
```

To run all the tests in a specific folder run

```bash
python -m unittest discover -s project_directory -p "test_*.py"
```

Read full test documentation [here](https://docs.python.org/3/library/unittest.html).

----
v : 0.0.8
