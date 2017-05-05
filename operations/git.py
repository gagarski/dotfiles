import os
import tempfile

from shutil import rmtree
from operations.base import Deploy, default_home, ExistsPolicy

from .directory import DeployDirectory


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


class DeployGitRepo(Deploy):
    def __init__(self,
                 repo,
                 dst,
                 checkout="master",
                 exists_policy=ExistsPolicy.MERGE,
                 home=default_home,
                 perms=int("755", 8)):

        super().__init__(home)
        self.repo = repo
        self.dst = dst
        self.checkout = checkout
        self.exists_policy = exists_policy
        self.perms = perms

    def run(self):
        dst_path = os.path.join(self.home, self.dst)
        if os.path.exists(dst_path):
            if self.exists_policy == ExistsPolicy.FAIL:
                raise FileExistsError("File or directory {} already exists".format(dst_path))
            elif self.exists_policy == ExistsPolicy.REMOVE and os.path.isdir(dst_path):
                rmtree(dst_path)
            elif self.exists_policy == ExistsPolicy.REMOVE:
                os.remove(dst_path)
            elif self.exists_policy == ExistsPolicy.MERGE and not os.path.exists(os.path.join(dst_path, ".git")):
                raise FileExistsError("File or directory {} exists and it's not a git repo".format(dst_path))
            else:
                _git_or_raise("checkout {}".format(self.checkout), dst_path)
                _git_or_raise("pull --ff-only", dst_path)
        else:
            os.makedirs(dst_path, self.perms)
            _git_or_raise("clone {} {}".format(self.repo, dst_path))
            _git_or_raise("checkout {}".format(self.checkout), dst_path)


class DeployFilesFromGitRepo(Deploy):
    def __init__(self,
                 repo,
                 dst,
                 checkout="master",
                 exists_policy="merge",
                 home=default_home,
                 perms=int("755", 8),
                 file_list=("*",)):
        super().__init__(home)
        self.repo = repo
        self.dst = dst
        self.checkout = checkout
        self.exists_policy = exists_policy
        self.perms = perms
        self.file_list = file_list

    def run(self):
        tempdir = tempfile.mkdtemp(prefix="dfd-temp")
        try:
            DeployGitRepo(repo=self.repo,
                          dst=os.path.join(tempdir, "repo"),
                          checkout=self.checkout,
                          exists_policy="remove",
                          home=self.home,  # Actually, we do not care here
                          perms=self.perms).run()
            dst_path = os.path.join(self.home, self.dst)
            os.makedirs(dst_path, self.perms, exist_ok=True)
            DeployDirectory(src=os.path.join(tempdir, "repo"),
                            home=dst_path,
                            exists_policy=self.exists_policy,
                            file_list=self.file_list).run()
        finally:
            if os.path.exists(tempdir):
                rmtree(tempdir)
