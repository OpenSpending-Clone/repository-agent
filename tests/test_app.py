import os
import shutil
import tempfile
import unittest
from test.support import EnvironmentVarGuard

from git.exc import GitCommandError

from repository_agent.app import \
    _get_repo_dir_path, _get_repo_remote, update_repo


class TestGetRepoPath(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('REPO_AGENT_BASE_DIR', '/path/to/specs')

    def test_path_success(self):
        valid_paths = [
            ['hi', '/path/to/specs/hi'],
            ['/My/Local/Path/To/repo', '/path/to/specs/repo'],
            ['https://github.com/brew/example-source-spec',
             '/path/to/specs/example-source-spec'],
            ['https://github.com/brew/example-source-spec.git?q=hi#asdf',
             '/path/to/specs/example-source-spec'],
            ['git@github.com:brew/example-source-spec.git?q=hi#asdf',
             '/path/to/specs/example-source-spec']
        ]

        with self.env:
            for input, returned in valid_paths:
                assert _get_repo_dir_path(input) == returned


class TestGetRepoBranch(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('REPO_AGENT_BASE_DIR', '/path/to/specs')

    def test_path_success(self):
        valid_paths = [
            ['hi', 'master'],
            ['/My/Local/Path/To/repo', 'master'],
            ['https://github.com/brew/example-source-spec', 'master'],
            ['https://github.com/brew/example-source-spec.git?q=hi#asdf',
             'asdf'],
            ['git@github.com:brew/example-source-spec.git?q=hi#asdf', 'asdf']
        ]

        with self.env:
            for input, returned in valid_paths:
                assert _get_repo_remote(input)[1] == returned


class TestGetRepoUrl(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('REPO_AGENT_BASE_DIR', '/path/to/specs')

    def test_path_success(self):
        valid_paths = [
            ['hi', 'hi'],
            ['/My/Local/Path/To/repo', '/My/Local/Path/To/repo'],
            ['https://github.com/brew/example-source-spec',
             'https://github.com/brew/example-source-spec'],
            ['https://github.com/brew/example-source-spec.git?q=hi#asdf',
             'https://github.com/brew/example-source-spec.git?q=hi'],
            ['git@github.com:brew/example-source-spec.git?q=hi#asdf',
             'git@github.com:brew/example-source-spec.git?q=hi']
        ]

        with self.env:
            for input, returned in valid_paths:
                assert _get_repo_remote(input)[0] == returned


class TestPullRepos(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.test_path = os.path.dirname(os.path.realpath(__file__))

        self.tmp_dir = tempfile.mkdtemp()

        # set up a local git repository for testing against.
        self.local_repo = os.path.join(self.test_path, 'data/local-example')
        # rename `git` to `.git` to make it a valid git repo
        os.rename(os.path.join(self.local_repo, 'dotgit'),
                  os.path.join(self.local_repo, '.git'))

        self.env.set('REPO_AGENT_BASE_DIR', self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        os.rename(os.path.join(self.local_repo, '.git'),
                  os.path.join(self.local_repo, 'dotgit'))

    def test_rel_path_success(self):
        with self.env:
            assert _get_repo_dir_path(self.local_repo) \
                == os.path.join(self.tmp_dir, 'local-example')

    def test_pull_local_repo(self):
        with self.env:
            # local repo doesn't exist yet
            assert not os.path.isdir(os.path.join(self.tmp_dir,
                                     'local-example'))

            update_repo(self.local_repo)

            # but does exist here
            assert os.path.isdir(os.path.join(self.tmp_dir, 'local-example'))
            assert os.path.exists(os.path.join(self.tmp_dir,
                                               'local-example/budget.csv'))

    def test_pull_local_twice(self):
        '''
        A change to a pulled file should be reverted to match the source
        repository when pulled again.
        '''
        with self.env:
            # pull local repo to tmp directory location
            update_repo(self.local_repo)

            original_file = os.path.join(self.local_repo, 'budget.csv')
            new_repo_file = os.path.join(self.tmp_dir,
                                         'local-example/budget.csv')

            # first line corresponds with original file
            with open(original_file) as org, open(new_repo_file) as new:
                assert org.readline() == new.readline()

            # change contents in new file
            with open(new_repo_file, 'w') as new:
                new.write('Changed contents of new file!')

            # first line is now different
            with open(original_file) as org, open(new_repo_file) as new:
                assert org.readline() != new.readline()

            # pull again (should change new file contents back to match repo)
            update_repo(self.local_repo)

            # first line corresponds with original file
            with open(original_file) as org, open(new_repo_file) as new:
                assert org.readline() == new.readline()

    def test_pull_non_existing_repo(self):
        '''
        An exception is raised if a non-existing repo update is attempted.
        '''
        with self.env, self.assertRaises(GitCommandError):
            update_repo('/my/local/path/to/nonexistent-repo')

    def test_pull_clean_on_update(self):
        '''
        If clean=True, remove untracked files during update.
        '''
        with self.env:
            # pull local repo to tmp directory location
            update_repo(self.local_repo)

            untracked_file = \
                os.path.join(self.tmp_dir, 'local-example/untracked.txt')

            # put an untracked file in there...
            with open(untracked_file, "w") as f:
                f.write("Untracked file!")
            assert os.path.exists(untracked_file)

            # pull again (without cleaning)
            update_repo(self.local_repo, clean=False)
            assert os.path.exists(untracked_file)

            # pull again (with clean)
            update_repo(self.local_repo, clean=True)
            assert not os.path.exists(untracked_file)
