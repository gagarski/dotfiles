import glob
import os
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file

from shutil import rmtree

import itertools
from stat import ST_MODE

from operations.base import Deploy, default_home, ExistsPolicy


class DeployDirectory(Deploy):
    def __init__(self, src, home=default_home, exists_policy=ExistsPolicy.MERGE, file_list=("*", ".*")):
        super().__init__(home)
        self.src = src
        self.exists_policy = exists_policy
        self.file_list = file_list

    @staticmethod
    def mkdirs_for_file(f, src, dst):
        src_path = os.path.join(src, f)
        dirs = []
        while len(f) > 0:
            parent = os.path.dirname(src_path)
            file = os.path.relpath(src_path, parent)
            mode = os.stat(src_path)[ST_MODE]
            dirs.append((file, mode))
            src_path = parent
            f = os.path.dirname(f)

        dirs = reversed(dirs[1:])
        current_dir = dst

        for (d, mode) in dirs:
            to_create = os.path.join(current_dir, d)
            os.mkdir(to_create, mode)
            current_dir = to_create

    def log(self):
        print("=" * 80)
        print(f"Deploying folder {self.src} into {self.home}.")
        print(f"Policy is {self.exists_policy}.")
        print(f"Files are {self.file_list}")
        print("=" * 80)

    def run(self):
        if not os.path.exists(self.src):
            raise FileNotFoundError("Directory {} does not exists".format(self.src))
        if not os.path.isdir(self.src):
            raise FileNotFoundError("{} is not a directory".format(self.src))
        for f in os.listdir(self.src):
            dst_path = os.path.join(self.home, f)
            if os.path.exists(dst_path):
                if self.exists_policy == ExistsPolicy.FAIL:
                    raise FileExistsError("File or directory {} already exists".format(dst_path))
                elif self.exists_policy == ExistsPolicy.REMOVE and os.path.isdir(dst_path):
                    rmtree(dst_path)
                elif self.exists_policy == ExistsPolicy.REMOVE:
                    os.remove(dst_path)

        files_to_copy = [os.path.relpath(h, self.src)
                         for h in itertools.chain(*[glob.glob(g)
                                                    for g in [os.path.join(self.src, f)
                                                              for f in self.file_list]])]

        for f in files_to_copy:
            dst_path = os.path.join(self.home, f)
            src_path = os.path.join(self.src, f)
            if os.path.isdir(src_path):
                copy_tree(src_path, dst_path)
            else:
                DeployDirectory.mkdirs_for_file(f, self.src, self.home)
                copy_file(src_path, dst_path)


class DeployDirectoryIfExists(Deploy):
    def __init__(self, src, home=default_home, exists_policy=ExistsPolicy.MERGE, file_list=("*", ".*")):
        super().__init__(home)
        self.src = src
        self.exists_policy = exists_policy
        self.file_list = file_list

    def log(self):
        print("=" * 80)
        print(f"Deploying folder {self.src} into {self.home}.")
        print(f"Policy is {self.exists_policy}.")
        print(f"Files are {self.file_list}")
        print("=" * 80)

    def run(self):
        if not os.path.exists(self.src):
            return

        if not os.path.isdir(self.src):
            return

        DeployDirectory(src=self.src,
                        home=self.home,
                        exists_policy=self.exists_policy,
                        file_list=self.file_list).run()
