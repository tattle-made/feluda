## setup:

1.  Setup virtual env

    `virtualenv --no-site-packages -p python3.6 .`

2.  Activate the env

    `source bin/activate`

3.  Install pip-tools.

    `pip install pip-tools`

4.  `requirements.in` should contain the high level packages that we want e.g.
    flask, numpy etc. `pip-compile` will generate `requirements.txt` which will
    have all the dependencies.

    `pip-compile requirements.in`

    `pip install -r requirements.txt`

5.  Run local server

    `python application.py`

## Developing Locally

```
docker-compose up
docker exec -it search_api python application.py
```

## Test API calls

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
