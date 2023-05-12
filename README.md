## Usage for local development with Docker

Previous requirements:

- Have docker-compose installed with pip.
- Have ports 8000 free

1. Start
```
docker-compose build
```

2. Run project

```
docker-compose up
```

#### Docker Workflow and tips: [link](documentation/readme/DOCKER_TIPS.md)

## API

Moni has an API which was created to serve multiple kind of devices, web, mobile, etc.

Moni's backend provides endpoints, which will be consumed by different sources.
The endpoints should return always all the fields, even if they are empty/null, this brings less problems when implementing a consumer.

You can check the [documentation here](documentation/readme/API_README.md).

## Testing

Running `pytest` on the main directory runs unit and bdd tests.

    pytest

Or individually

    pytest apps/tests/*.py  # Only unit tests

##### Access to the API Docs interface

```
http://0.0.0.0:8000/docs
```
