import os
from urllib.parse import urlparse

from git import Repo
from dotenv import load_dotenv

import logging
log = logging.getLogger(__name__)

load_dotenv()


def _get_repo_dir_path(url):
    '''
    For a given git url, return the local repo directory path. This is based on
    the 'humanish' repo directory name and the REPO_AGENT_BASE_DIR.
    '''
    BASE_DIR = os.environ['REPO_AGENT_BASE_DIR']
    repo_dir = os.path.basename(urlparse(url).path).split('.')[0]
    return os.path.join(BASE_DIR, repo_dir)


def update_repo(repo_url):
    '''
    Update an individual repo.
    '''
    repo_path = _get_repo_dir_path(repo_url)
    # If repo_path doesn't exist, create it.
    if not os.path.isdir(repo_path):
        os.makedirs(repo_path)

    # If repo_path empty, clone repo_url into it.
    if not os.listdir(repo_path):
        log.info('Cloning {}'.format(repo_url))
        Repo.clone_from(repo_url, repo_path, branch='master')
    # If repo_path isn't empty...
    else:
        repo = Repo(repo_path)
        # This repo's remote corresponds with repo_url, force pull it.
        if repo_url == repo.remotes.origin.url:
            log.info('Updating "{}" from {}'.format(repo_path, repo_url))
            repo.git.clean('-d', '-f')
            repo.head.reset(index=True, working_tree=True)
            repo.remotes.origin.pull()
