## [Requirement](requirement.md)

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

## Access to the API Docs interface

```
http://0.0.0.0:8000/docs
```

## Testing

Running `pytest` on the main directory runs tests.

    pytest

Or individually

    pytest apps/tests/*.py  # Only unit tests
