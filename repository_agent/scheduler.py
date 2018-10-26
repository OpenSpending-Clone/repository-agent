from envparse import env
from celery import Celery

from repository_agent.app import _pull_repo

REPOS = env('REGISTRY_REPOS', cast=list, subcast=str)
UPDATE_FREQUENCY = env.int('REGISTRY_UPDATE_FREQUENCY', default=30)
BROKER = env('REGISTRY_BROKER')

celeryapp = Celery(broker=BROKER)


@celeryapp.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(int(UPDATE_FREQUENCY), pull_repos.s(REPOS))


@celeryapp.task
def pull_repos(repos):
    for repo_url in repos:
        update_repo.apply_async((repo_url, ))


@celeryapp.task
def update_repo(repo_url):
    _pull_repo(repo_url)
