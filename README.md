# minimal-api

## Installation
- Clone this repo
- Create virtual environment using `virtualenv`
- Install 


## Running tests
```shell
make test
```

## Development with docker
```shell
make dev
```

## Invoking API

### Create Recipe API
```shell
curl -XPOST -H "Content-type: application/json" -d '{
    "url": "https://werkzeug.palletsprojects.com/en/2.0.x/wrappers/"
}' 'http://localhost:5000/url/'
```

### List Recipe API
```shell
curl -XGET -H "Content-type: application/json" -d '{
    "url": "https://werkzeug.palletsprojects.com/en/2.0.x/wrappers/"
}' 'http://localhost:5000/url/c+'
```
