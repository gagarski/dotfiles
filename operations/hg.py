import os
import tempfile

from shutil import rmtree

from operations import DeployVcsRepo, DeployFilesFromVcsRepo
from operations.base import Deploy, default_home, ExistsPolicy

from .directory import DeployDirectory


class HgException(Exception):
    def __init__(self, op, ret):
        super().__init__("""Operation "hg {}" failed with code {}""".format(op, ret))


def _hg(op, repo_path=None):
    if repo_path:
        return os.system("hg -R {} {}".format(repo_path, op))
    else:
        return os.system("hg {}".format(op))


def _hg_or_raise(op, repo_path=None):
    ret = _hg(op, repo_path)
    if ret != 0:
        raise HgException(op, ret)


class DeployHgRepo(DeployVcsRepo):
    def __init__(self,
                 repo,
                 dst,
                 update="default",
                 exists_policy=ExistsPolicy.MERGE,
                 home=default_home,
                 perms=int("755", 8)):

        super().__init__(repo, dst, exists_policy, home, perms)
        self.update = update

    @property
    def vcs_name(self):
        return "hg"

    def vcs_log(self):
        print(f"Updating to {self.update}")

    def clone(self, path):
        _hg_or_raise("clone {} {}".format(self.repo, path))
        _hg_or_raise("update {}".format(self.update), path)

    def update_existing(self, path):
        _hg_or_raise("update {}".format(self.update), path)
        _hg_or_raise("pull -u", path)

    def is_path_repo(self, path):
        return os.path.exists(os.path.join(path, ".hg"))


class DeployFilesFromHgRepo(DeployFilesFromVcsRepo):
    def __init__(self,
                 repo,
                 dst,
                 update="default",
                 exists_policy=ExistsPolicy.MERGE,
                 home=default_home,
                 perms=int("755", 8),
                 file_list=("*", ".*")):
        super().__init__(repo, dst, exists_policy, home, perms, file_list)
        self.update = update

    @property
    def vcs_name(self):
        return "hg"

    def vcs_log(self):
        print(f"Updating to {self.update}")

    def vcs_operation(self, dst):
        return DeployHgRepo(repo=self.repo,
                            dst=os.path.join(dst, "repo"),
                            update=self.update,
                            exists_policy=ExistsPolicy.REMOVE,
                            home=self.home,  # Actually, we do not care here
                            perms=self.perms)
