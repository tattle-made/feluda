```
curl es:9200
curl es:9200/_aliases?pretty=true

# DELETE
curl -XDELETE es:9200/txtsearch
curl -XDELETE es:9200/imgsearch
curl -XDELETE es:9200/vidsearch

# SIMPLE TEXT QUERY
curl -X GET "localhost:9200/txtsearch/_search?pretty"

curl -X GET "localhost:9200/my-index-000001/_search?pretty"
```
