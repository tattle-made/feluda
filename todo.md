# TODO
- scraping online content
- test on server/AWS
- add video support
- add audio support

# Questions/not immediate thoughts
- types of preprocessing for text/image/media/audio that does not change them for a user?
- what is the similarity threshold?
- What schema to use? Store original files as backup on S3?
- supporting various formats of media
- multilingual text extraction / open-source OCR?

# mongo
- install mongo on wsl:
    - used this: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
    - then this: https://github.com/michaeltreat/Windows-Subsystem-For-Linux-Setup-Guide/blob/master/readmes/installs/MongoDB.md
    - https://github.com/michaeltreat/Mongo_CheatSheet
- run mongo server:
    - sudo mongod --dbpath ~/data/db
    - run create_mongo_db()  

# tesseract ocr
[install](https://github.com/tesseract-ocr/tesseract): 
- sudo apt-get install tesseract-ocr  
or 
- pip install tesseract-ocr

# environment files
- .env
- env_template

# firebase
- hook to firebase: https://stackoverflow.com/questions/40799258/where-can-i-get-serviceaccountcredentials-json-for-firebase-admin

# testing
python -m applicationTests
python -m dbTests