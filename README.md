# Git Repository Agent

[![Travis](https://img.shields.io/travis/frictionlessdata/datapackage-pipelines-registry-agent/master.svg)](https://travis-ci.org/frictionlessdata/datapackage-pipelines-registry-agent)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/datapackage-pipelines-registry-agent/master.svg)](https://coveralls.io/r/frictionlessdata/datapackage-pipelines-registry-agent?branch=master)
[![PyPi](https://img.shields.io/pypi/v/datapackage-pipelines-registry-agent.svg)](https://pypi.python.org/pypi/datapackage-pipelines-registry-agent)
[![SemVer](https://img.shields.io/badge/versions-SemVer-brightgreen.svg)](http://semver.org/)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)


Keep a local registry of git repositories up to date, using Celery as a scheduler.

## Install

```
# clone the repo and install with pip

git clone https://github.com/frictionlessdata/datapackage-pipelines-registry-agent.git
pip install -e .
```

## Usage

### Configuration

Settings can be configured via environmental variables.

```sh
REGISTRY_BASE_DIR: /app/repositories  # Directory to clone repos to

# If using the celery scheduler
REGISTRY_UPDATE_FREQUENCY: 300  # Frequency, in seconds, for updating the registry.
REGISTRY_BROKER: redis://redis:6379/10  # URL for the redis task broker
REGISTRY_REPOS: https://github.com/example1/example-repo, https://github.com/example2/example-repo  # List of repositories separated by commas
```

### Local development

Use the provided `docker-compose.yml` file to start the application with the celery scheduler.

```sh
$ docker-compose -f docker-compose.yml up
```
