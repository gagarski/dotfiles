import os
import tempfile

from shutil import rmtree
from operations.base import Deploy, default_home, ExistsPolicy

from operations.directory import DeployDirectory


class DeployVcsRepo(Deploy):
    def __init__(self,
                 repo,
                 dst,
                 exists_policy=ExistsPolicy.MERGE,
                 home=default_home,
                 perms=int("755", 8)):

        super().__init__(home)
        self.repo = repo
        self.dst = dst
        self.exists_policy = exists_policy
        self.perms = perms

    @property
    def vcs_name(self):
        raise NotImplementedError("Implement me in subclasses")

    def update_existing(self, path):
        raise NotImplementedError("Implement me in subclasses")

    def clone(self, path):
        raise NotImplementedError("Implement me in subclasses")

    def vcs_log(self):
        pass

    def is_path_repo(self, path):
        raise NotImplementedError("Implement me in subclasses")

    def log(self):
        print("=" * 80)
        print(f"Deploying {self.vcs_name} repo {self.repo} into {self.dst} at {self.home}.")
        print(f"Policy is {self.exists_policy}.")
        print(f"Permissions for destination are {oct(self.perms)}")
        self.vcs_log()
        print("=" * 80)

    def run(self):
        dst_path = os.path.join(self.home, self.dst)
        if os.path.exists(dst_path):
            if self.exists_policy == ExistsPolicy.FAIL:
                raise FileExistsError("File or directory {} already exists".format(dst_path))
            elif self.exists_policy == ExistsPolicy.REMOVE and os.path.isdir(dst_path):
                rmtree(dst_path)
            elif self.exists_policy == ExistsPolicy.REMOVE:
                os.remove(dst_path)
            elif self.exists_policy == ExistsPolicy.MERGE and not self.is_path_repo(dst_path):
                raise FileExistsError(f"File or directory {dst_path} exists and it's not a {self.vcs_name} repo")
            else:
                self.update_existing(dst_path)
        else:
            os.makedirs(dst_path, self.perms)
            self.clone(dst_path)


class DeployFilesFromVcsRepo(Deploy):
    def __init__(self,
                 repo,
                 dst,
                 exists_policy=ExistsPolicy.MERGE,
                 home=default_home,
                 perms=int("755", 8),
                 file_list=("*", ".*")):
        super().__init__(home)
        self.repo = repo
        self.dst = dst
        self.exists_policy = exists_policy
        self.perms = perms
        self.file_list = file_list

    def vcs_log(self):
        pass

    def log(self):
        print("=" * 80)
        print(f"Deploying files {self.file_list} from {self.repo} into {self.dst} at {self.home}.")
        print(f"Policy is {self.exists_policy}.")
        print(f"Permissions for temporary destination  are {oct(self.perms)}")
        self.vcs_log()
        print("=" * 80)

    def vcs_operation(self, dst):
        raise NotImplementedError("Implement me in subclasses")

    def run(self):
        tempdir = tempfile.mkdtemp(prefix="dfd-temp")
        try:
            self.vcs_operation(os.path.join(tempdir, "repo")).run()
            dst_path = os.path.join(self.home, self.dst)
            os.makedirs(dst_path, self.perms, exist_ok=True)
            DeployDirectory(src=os.path.join(tempdir, "repo"),
                            home=dst_path,
                            exists_policy=self.exists_policy,
                            file_list=self.file_list).run()
        finally:
            if os.path.exists(tempdir):
                rmtree(tempdir)
