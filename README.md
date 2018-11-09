# Git Repository Agent

[![Travis](https://img.shields.io/travis/openspending/repository-agent/master.svg)](https://travis-ci.org/openspending/repository-agent)
[![Coveralls](http://img.shields.io/coveralls/openspending/repository-agent/master.svg)](https://coveralls.io/r/openspending/repository-agent?branch=master)
[![SemVer](https://img.shields.io/badge/versions-SemVer-brightgreen.svg)](http://semver.org/)
[![Gitter](https://img.shields.io/gitter/room/openspending/chat.svg)](https://gitter.im/openspending/chat)


Keep a local registry of git repositories up to date, using Celery as a scheduler.

## Install

```
# clone the repo and install with pip

git clone https://github.com/openspending/repository-agent.git
pip install -e .
```

## Usage

### Configuration

Settings can be configured via environmental variables.

```sh
REPO_AGENT_BASE_DIR: /app/repositories  # Directory to clone repos to

# If using the celery scheduler
REPO_AGENT_CLEAN_ON_UPDATE: False  # Clean local repos during update (removes local untracked files)
REPO_AGENT_UPDATE_FREQUENCY: 300  # Frequency, in seconds, for updating the registry.
REPO_AGENT_BROKER: redis://redis:6379/10  # URL for the redis task broker
REPO_AGENT_REPOS: https://github.com/example1/example-repo, https://github.com/example2/example-repo#branch  # List of repositories separated by commas
```

### Resetting the repos

Sometimes the automatically fetched repositories get into a state where they are in conflict with the upstream origin and updates can't be pulled. For example, if pulls require a merge conflict to be resolved, or if someone force pushed to the origin. The quickest way to resolve this is simply to remove the affected cloned repository, and allow repository-agent to repopulate it:

```sh
$ rm -rf /app/repositories/affected-repo
```

### Local development

Use the provided `docker-compose.yml` file to start the application with the celery scheduler.

```sh
$ docker-compose -f docker-compose.yml up
```
