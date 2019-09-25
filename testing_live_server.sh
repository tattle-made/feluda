#!/bin/bash

# how-to
# https://askubuntu.com/questions/420981/how-do-i-save-terminal-output-to-a-file

# NOTE: saving with LF endings for executing in bash, also .env

# define vars
OUT_FILE=tests/testing_live_server.out
ERR_FILE=tests/testing_live_server.err

# files
image_with_text_url=https://tattle-services.s3.ap-south-1.amazonaws.com/28bfb060-c51f-11e9-909c-fb10cde080ad

# replace env vars with local .env
. .env

# https://stackoverflow.com/questions/35018899/using-curl-in-a-bash-script-and-getting-curl-3-illegal-characters-found-in-ur
# LIVE_SERVER=${LIVE_SERVER%$'\r'}

# find_text
curl -X POST $LIVE_SERVER/find_text -H "Content-Type: application/json" -d '{"image_url": "'$image_with_text_url'"}' >$OUT_FILE 2>$ERR_FILE

# find_duplicate text
curl -X POST $LIVE_SERVER/find_duplicate -H "Content-Type:application/json" -d '{"text": "i like pie"}' >>$OUT_FILE 2>>$ERR_FILE

# find_duplicate image
curl -X POST $LIVE_SERVER/find_duplicate -H "Content-Type: application/json" -d '{"image_url": "'$image_with_text_url'"}' >>$OUT_FILE 2>>$ERR_FILE

# upload_text
curl -X POST $LIVE_SERVER/upload_text -H "Content-Type: application/json" -d '{"text": "this is absolutely english text!"}' >>$OUT_FILE 2>>$ERR_FILE

# upload_image
curl -X POST $LIVE_SERVER/upload_image -H "Content-Type: application/json" -d '{"image_url": "'$image_with_text_url'"}' >>$OUT_FILE 2>>$ERR_FILE

# update_tags
curl -X POST $LIVE_SERVER/update_tags -H "Content-Type: application/json" -d '{"doc_id": 1, "tags": "['fast']"}' >>$OUT_FILE 2>>$ERR_FILE

