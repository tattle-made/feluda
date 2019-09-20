# TODO
- host a dataset for loading/testing the database on S3
    - data source: reddit? sharechat?
- test on server/AWS
- run/test with mongodb
- add video support
- add audio support

# Questions/not immediate thoughts
- How to display approximate matches, what is the threshold?
- What schema to use? Should original files and images be stored in the same db? Which backend to use?
- standardized form of storing text, audio, video data
    - or pipeline to incorporate formats into db
- multilingual text extraction / open-source OCR?
- approximate match resistant to small changes in input file
