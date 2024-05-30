# Schedulify: Architecture overview #

We use [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) to run all application components and backing services in isolated environment.

## Software versions ##

* Python **[3.11](https://docs.python.org/)**, installed via [pyenv](https://github.com/pyenv/pyenv).
* Django **[4.2.11](https://docs.djangoproject.com/)**, installed via [pip](https://pypi.python.org/pypi) - official Python package index.
* Celery **[latest stable](http://docs.celeryproject.org/en/latest/index.html)**, installed via [pip](https://pypi.python.org/pypi) - official Python package index.
* Postgres **[15.0](https://www.postgresql.org/docs/15.0/static/index.html)**, installed via [official Docker image](https://hub.docker.com/_/postgres).
* Redis **[7.0](https://redis.io/)**, installed via [official Docker image](https://hub.docker.com/_/redis).

## Postgres databases ##

| DB name | Description | Owner |
| ------- | ----------- | ----- |
| `schedulify_db` | database for main application | `postgres` |

## Redis databases ##

| DB number | Usage |
| --------- | ----- |
| `0` | Not used |
| `1` | Celery broker |
| `2` | Direct usage with [`redis_client`](./api/schedulify/apps/common/utils/redis.py#L9) function in main application |
| `3` - `15` | Not used |
