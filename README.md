# Buildings Service
## Overview
The Buildings Service contains a REST API and a GraphQL API and is built up of three basic components:

* Building
* Meter
* Meter Readings

The service uses an sql lite database that is populated when the docker container is started.

## Installation
The service is ran inside docker and contains a docker compose file.

`docker-compose up -d`

And runs on port 8000.

## API
The REST API has the following endpoints:

```
/building
/meter
/meter_reading
```

The GraphQL schema is at `/graphql` and contains a graphql playground that can be viewed in the browser.
The schema can be found in `schema.graphql`.
