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
  $ pip install  --require-hashes --no-deps -r requirements.txt
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
  $ pip install  --require-hashes --no-deps -r image_vec_rep_resnet_requirements.txt
  $ pip install  --require-hashes --no-deps -r vid_vec_rep_resnet_requirements.txt
..
# Create the docker containers
  $ cd src/api/
  $ docker build -t image-operator -f Dockerfile.image_vec_rep_resnet .
  $ docker build -t video-operator -f Dockerfile.vid_vec_rep_resnet .
# Run the docker image
  $ docker run image-operator
  $ docker run video-operator
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
- If an operator defaults to a higher version than allowed by feluda core `requirements.txt`, manually edit the `<operator>_requirements.txt` to the compatible version. Then run `pip install`. If it runs without errors, the package version is valid for the operator.

```bash
$ cd src/
$ pip install --upgrade pip-tools
$ TMPDIR=<temp_dir> pip-compile --verbose --allow-unsafe --generate-hashes --emit-index-url --emit-find-links requirements.in

# Updating operators
$ cd src/core/operators/
# The link for torch is required since PyPi only hosts the GPU version of torch packages.
$ TMPDIR=<temp_dir> pip-compile --verbose --allow-unsafe --generate-hashes --emit-index-url --emit-find-links --find-links https://download.pytorch.org/whl/torch_stable.html vid_vec_rep_resnet_requirements.in
$ TMPDIR=<temp_dir> pip-compile --verbose --allow-unsafe --generate-hashes --emit-index-url --emit-find-links --find-links https://download.pytorch.org/whl/torch_stable.html audio_vec_embedding_requirements.in
```

#### Modify generated `requirements.txt` for platform specific torch packages

NOTE: Update the command to match python docker image version

```bash
# Download package to find hash - you will get an error message if the package has been previously downloaded without the hash. The hash value will be printed in the message. Use that hash

$ pip download --no-deps --require-hashes --python-version 311 --implementation cp --abi cp311 --platform linux_x86_64 --find-links https://download.pytorch.org/whl/torch_stable.html torch==2.2.0+cpu
$ pip download --no-deps --require-hashes --python-version 311 --implementation cp --abi cp311 --platform linux_x86_64 --find-links https://download.pytorch.org/whl/torch_stable.html torchvision==0.17.0+cpu
$ pip download --no-deps --require-hashes --python-version 311 --implementation cp --abi cp311 --platform manylinux2014_aarch64 --find-links https://download.pytorch.org/whl/cpu torch==2.2.0
$ pip download --no-deps --require-hashes --python-version 311 --implementation cp --abi cp311 --platform manylinux2014_aarch64 --find-links https://download.pytorch.org/whl/cpu torchvision==0.17.0
```
Replace the torch package lines from `requirement.txt` with the following (depending upon the generated hash values above)

```bash
# For arm64 architecture
--find-links https://download.pytorch.org/whl/cpu
torch==2.2.0; platform_machine=='aarch64' \
    --hash=sha256:9328e3c1ce628a281d2707526b4d1080eae7c4afab4f81cea75bde1f9441dc78
    # via
    #   -r vid_vec_rep_resnet_requirements.in
    #   torchvision
torchvision==0.17.0; platform_machine=='aarch64' \
    --hash=sha256:3d2e9552d72e4037f2db6f7d97989a2e2f95763aa1861963a3faf521bb1610c4 \
    # via -r vid_vec_rep_resnet_requirements.in

# For amd64 architecture
--find-links https://download.pytorch.org/whl/torch_stable.html
torch==2.2.0+cpu; platform_machine=='x86_64' \
    --hash=sha256:15a657038eea92ac5db6ab97b30bd4b5345741b49553b2a7e552e80001297124 \
    --hash=sha256:15e05748815545b6eb99196c0219822b210a5eff0dc194997a283534b8c98d7c \
    --hash=sha256:2a8ff4440c1f024ad7982018c378470d2ae0a72f2bc269a22b1a677e09bdd3b1 \
    --hash=sha256:4ddaf3393f5123da4a83a53f98fb9c9c64c53d0061da3c7243f982cdfe9eb888 \
    --hash=sha256:58194066e594cd8aff27ddb746399d040900cc0e8a331d67ea98499777fa4d31 \
    --hash=sha256:5b40dc66914c02d564365f991ec9a6b18cbaa586610e3b160ef559b2ce18c6c8 \
    --hash=sha256:5f907293f5a58619c1c520380f17641f76400a136474a4b1a66c363d2563fe5e \
    --hash=sha256:8258824bec0181e01a086aef5809016116a97626af2dcbf932d4e0b192d9c1b8 \
    --hash=sha256:d053976a4f9ca3bace6e4191e0b6e0bcffbc29f70d419b14d01228b371335467 \
    --hash=sha256:f72e7ce8010aa8797665ff6c4c1d259c28f3a51f332762d9de77f8a20277817f
    # via
    #   -r vid_vec_rep_resnet_requirements.in
    #   torchvision
torchvision==0.17.0+cpu; platform_machine=='x86_64' \
    --hash=sha256:00e88e9483e52f99fc61a73941b6ef0b59d031930276fc220ee8973170f305ff \
    --hash=sha256:04e72249add0e5a0fc3d06a876833651e77eb6c3c3f9276e70d9bd67804c8549 \
    --hash=sha256:39d3b3a80c63d18594e81829fdbd6108512dff98fa17156c7bec59133a0c1173 \
    --hash=sha256:55660c67bd8d5b777984655116b75070c73d37ce64175a8120cb59010039fd7f \
    --hash=sha256:569ebc5f47bb765ae73cd380ace01ddcb074c67df05d7f15f5ddd0fa3062881a \
    --hash=sha256:701d7fcfdd8ed206dcb71774190152f0a2d6c999ad7cee277fc5a71a943ae64d \
    --hash=sha256:b683d52753c5579a5b0250d7976deada17deab646071da289bd598d1af4877e0 \
    --hash=sha256:bb787aab6daf2d72600c14cd7c3c11459701dc5fac07e790e0335777e20b39df \
    --hash=sha256:da83b8a14d1b0579b1119e24272b0c7bf3e9ad14297bca87184d02c12d210501 \
    --hash=sha256:eb1e9d061c528c8bb40436d445599ca05fa997701ac395db3aaec5cb7660b6ee
    # via -r vid_vec_rep_resnet_requirements.in
```



#### Updating specific packages in `requirements.txt`

This is useful to update dependencies e.g. when using `pip-audit`

```bash
$ TMPDIR=<temp_dir> pip-compile --verbose --allow-unsafe --generate-hashes --find-links https://download.pytorch.org/whl/torch_stable.html --upgrade-package <package>==<version> --upgrade-package <package>

```

### Running Tests

To run a test, implement the following command.

```bash
python -m unittest <FILE_NAME>.py
```

To run all the tests in a specific folder run

```bash
python -m unittest discover -s project_directory -p "test_*.py"
```

Read full test documentation [here](https://github.com/tattle-made/feluda/wiki/Running-Tests).

----
v : 0.0.8
