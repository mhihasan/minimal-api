# minimal-api

## Invoking API

### Create Short Url
```shell
curl -XPOST -H "Content-type: application/json" -d '{
    "url": "https://werkzeug.palletsprojects.com/en/2.0.x/wrappers/"
}' 'http://localhost:5000/url/'
```

### Short URL details
```shell
curl -XGET -H "Content-type: application/json" -d '{
    "url": "https://werkzeug.palletsprojects.com/en/2.0.x/wrappers/"
}' 'http://localhost:5000/url/c+'
```
