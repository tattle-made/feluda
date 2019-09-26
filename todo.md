# TODO
- dataset for testing on S3
    - 50 images with text: hindi, guj, eng, tam, mal, tel, pun, bang
        - diff image formats
        - diff image preprocessing
    - diff formats/scripts/encoding of text
- test on server/AWS
- add video support
- add audio support

# Questions/not immediate thoughts
- How to display approximate matches, what is the threshold?
- What schema to use? Store original files as backup on S3? Which backend to use?
- supporting various formats of media
- multilingual text extraction / open-source OCR?
- approximate match resistant to small changes in input file

# mongo
- install mongo on wsl:
    - used this: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
    - then this: https://github.com/michaeltreat/Windows-Subsystem-For-Linux-Setup-Guide/blob/master/readmes/installs/MongoDB.md
    - https://github.com/michaeltreat/Mongo_CheatSheet
- run mongo server:
    - sudo mongod --dbpath ~/data/db
    - run create_mongo_db()  

# environment files
- .env
- env_template

# firebase
- hook to firebase: https://stackoverflow.com/questions/40799258/where-can-i-get-serviceaccountcredentials-json-for-firebase-admin
