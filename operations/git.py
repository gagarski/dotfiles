import os

from operations.base import default_home, ExistsPolicy
from operations.vcs import DeployVcsRepo, DeployFilesFromVcsRepo


class GitException(Exception):
    def __init__(self, op, ret):
        super().__init__("""Operation "git {}" failed with code {}""".format(op, ret))


def _git(op, repo_path=None):
    if repo_path:
        return os.system("git -C {} {}".format(repo_path, op))
    else:
        return os.system("git {}".format(op))


def _git_or_raise(op, repo_path=None):
    ret = _git(op, repo_path)
    if ret != 0:
        raise GitException(op, ret)


class DeployGitRepo(DeployVcsRepo):
    def __init__(self,
                 repo,
                 dst,
                 checkout="master",
                 exists_policy=ExistsPolicy.MERGE,
                 home=default_home,
                 perms=int("755", 8)):

        super().__init__(repo, dst, exists_policy, home, perms)
        self.checkout = checkout

    @property
    def vcs_name(self):
        return "git"

    def vcs_log(self):
        print(f"Checking out {self.checkout}")

    def clone(self, path):
        _git_or_raise("clone {} {}".format(self.repo, path))
        _git_or_raise("checkout {}".format(self.checkout), path)

    def is_path_repo(self, path):
        return os.path.exists(os.path.join(path, ".git"))

    def update_existing(self, path):
        _git_or_raise("checkout {}".format(self.checkout), path)
        _git_or_raise("pull --ff-only", path)


class DeployFilesFromGitRepo(DeployFilesFromVcsRepo):
    def __init__(self,
                 repo,
                 dst,
                 checkout="master",
                 exists_policy=ExistsPolicy.MERGE,
                 home=default_home,
                 perms=int("755", 8),
                 file_list=("*", ".*")):
        super().__init__(repo, dst, exists_policy, home, perms, file_list)
        self.checkout = checkout

    @property
    def vcs_name(self):
        return "git"

    def vcs_log(self):
        print(f"Checking out {self.checkout}")

    def vcs_operation(self, dst):
        return DeployGitRepo(repo=self.repo,
                             dst=os.path.join(dst, "repo"),
                             checkout=self.checkout,
                             exists_policy=ExistsPolicy.REMOVE,
                             home=self.home,  # Actually, we do not care here
                             perms=self.perms)
