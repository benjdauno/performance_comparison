# Gunicorn Worker, Container Replica & Database Connection Comparison

This repo is put together to explore the performance tradeoffs between running a Flask app with multiple workers vs. a single worker per container, while also varying things like the database connection pools, and the number of containers.

## Prerequisites

This setup requires:

- Docker & docker compose
- k6 load testing tool

Docker should already be installed via your engineering laptop setup, and k6 can be installed with brew.

```
brew install k6
```

## Context

This setup uses docker compose to run a simple Flask app via Gunicorn that simulates I/O heavy workloads, a MySQL database, and an nginx container to act as a load balancer between 1-2 replicas of the Flask app.

K6 is then used to throw traffic at the app, so we can measure the performance difference between different configurations. The primary areas of experimentation are currently:

- number of Gunicorn workers per container
- number of database connections allowed per Flask app
- number of containers

However, this is likely to expand.

## Getting started

There's a Makefile that includes all the commands that are needed to get going.

1. ```make build``` to build and star the docker containers
2. ```make test``` to run k6 against the environment


## Caveats

Load balancing between multiple docker containers running the Flask app currently only works with 1 or 2 containers. The likely reason for this is docker embedded DNS, which causes some of the container IP addresses to just not be used by k6.

If this needs to be corrected and more than2 replicas of the Flask app are needed, manually copy the flask app service block, increment the service name, and then manually add entries to the nginx.conf file.