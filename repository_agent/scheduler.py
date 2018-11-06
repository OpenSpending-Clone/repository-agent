from envparse import env
from celery import Celery

from git.exc import GitCommandError, InvalidGitRepositoryError

from repository_agent.app import update_repo

import logging
log = logging.getLogger(__name__)


REPOS = env('REPO_AGENT_REPOS', cast=list, subcast=str)
UPDATE_FREQUENCY = env.int('REPO_AGENT_UPDATE_FREQUENCY', default=30)
BROKER = env('REPO_AGENT_BROKER')
CLEAN_ON_UPDATE = env('REPO_AGENT_CLEAN_ON_UPDATE', cast=bool, default=False)

celeryapp = Celery(broker=BROKER)


@celeryapp.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(int(UPDATE_FREQUENCY), update_all_repos.s(REPOS))


@celeryapp.task
def update_all_repos(repos):
    for repo_url in repos:
        update_repo_task.apply_async((repo_url, ))


@celeryapp.task
def update_repo_task(repo_url):
    try:
        update_repo(repo_url, clean=CLEAN_ON_UPDATE)
    except (GitCommandError, InvalidGitRepositoryError) as e:
        log.error('Repo update failed. Logging and moving on...')
        log.error(e)
